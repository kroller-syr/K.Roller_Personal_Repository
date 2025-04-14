#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Project Name: IST 736 Homework 2
#Author: Kent Roller
#Date: 01/13/25
#Description: Import tweet database from outside source. Perform pre processing on data and prepare 
# text for sentiment analysis.Perform vectorization on text, examine vectorization and compare to results
# from the sentiment analysis. 


# In[2]:


#First need to import the csv file containing the tweets
#since the file is local can import from file path
import pandas as pd 
#specify the file path
file_path = "C:/Users/super/OneDrive/Desktop/Chatgpt_Tweets_Nov30_Feb11.csv"
#load the file_path
#Need to specify encoding for some reason with this file
tweets_df = pd.read_csv(file_path, encoding='ISO-8859-1')
#Print head to make sure import and load is succesful
print(tweets_df.head())
#Correct encoding may not be selected as there are still some wonky characters but the file only produced 
# an error before using the encoding argument. Since the rest can be removed by other means will
# accept this though I realize it may not be optimal


# In[3]:


#Using ISO-8859-1 as the encoding seemed to work, though from the print out we can see that there are 
# characters that will need to be removed. Fortunately, since we are focused on the tweets themselves, 
# the rest of the data is not necessary, at least for our intent. 
#Now we will seperate the text column from the rest of the df
tweets_text_df = tweets_df[['Text']]

#Print out the head to make sure seperation is correct
print(tweets_text_df.head())


# In[4]:


#Now we need to resolve another issue. There are non-ASCII characters in the text. 
#These will need to be removed before we can perform any meaningful analysis. 
#Create function to clean text of non ASCII characters using REGEX:
import re
def clean_text(text):
    #REGEX for removing NON ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

#Apply the cleaning function 
tweets_text_df['Text'] = tweets_text_df['Text'].apply(clean_text)

#Print the head top make sure NON ASCII characters were removed correctly 
print(tweets_text_df.head())


# In[12]:


#oops, may need to install vader package first before trying to import
#!pip install scikit-learn nltk vaderSentiment


# In[5]:


#Okay, this looks much better. Now we can begin the actual pre processing to prepare the text
# for sentiment analysis
#First need to import required packages and resources
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import nltk

#Need stopwords 
nltk.download('punkt')
nltk.download('stopwords')

#Intialize the stopwords collection to english since this is the target langauge
stop_words = set(stopwords.words('english'))


# In[6]:


#Now need to clean and tokenize the text
def preprocess_text(text):
    #tokenize the text, convert all to lower case
    tokens = word_tokenize(text.lower())
    #Remove stop words and other items missed by the REGEX if any
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)

#Apply function to the text column in the df (the only column in our new df)
tweets_text_df['cleaned_text'] = tweets_text_df['Text'].apply(preprocess_text)


# In[7]:


#Now need to vectorize the tokens 
from sklearn.feature_extraction.text import CountVectorizer

#Initialize CountVectorizer
count_vect = CountVectorizer()
#Fit and transform the cleaned text from previous step
x_count = count_vect.fit_transform(tweets_text_df['cleaned_text'])


# In[12]:


#Initialize VADER sentiment analysis
#Note, the vader sentimentintensityanalyzer was loaded in a previous step, so it is already called 
#versus the nltk which will be called below
vdr_analyzer = SentimentIntensityAnalyzer()

#After some reading of the docs it looks like vdr works with pre-processed text 
#but does not need to be vectorized in order to do so. 
#since this is the case we will just use the pre-processed text stored in 
#cleaned_text for the sentiment analysis. The same may be true for NLTK. 
#Also need to go back and look at the requirements for the assigment. 
#

#Pull the sentiment scores 
def get_sent_score(text):
    #set the score metric to be based on the polarity score 
    scores = vdr_analyzer.polarity_scores(text)
    return scores['compound']

#Apply vader
tweets_text_df['vdr_sentiment_score'] = tweets_text_df['cleaned_text'].apply(get_sent_score)

#Add labels to the sentiment scores for easy digestion or visualization 
def label_sent(score):
    if score > 0.00:
        return 'positive'
    elif score < 0.00:
        return 'negative'
    else:
        return 'neutral'

#Apply the labels to the scores stored in the df under the variable name vdr_sentiment_score
tweets_text_df['vdr_sent_label'] = tweets_text_df['vdr_sentiment_score'].apply(label_sent) 


# In[13]:


#Now need to make sure that changes applied have been succesful 
print(tweets_text_df.head(10))
#Hmmm, looks like I goofed on the split for the labels. Vader appears to use a -1 to 1 range for
#scoring so label needs to reflect this, otherwise negative will be false high value


# In[21]:


from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the required NLTK resources
nltk.download('vader_lexicon')

# Initialize the NLTK Sentiment Intensity Analyzer
nltk_analyzer = SentimentIntensityAnalyzer()

# Define the function for NLTK sentiment score
def nltk_get_sent_score(text):
    # Calculate polarity score using NLTK
    nltk_scores = nltk_analyzer.polarity_scores(text)
    return nltk_scores['compound']

# Add labels to the sentiment scores
def nltk_label_sent(nltk_score):
    if nltk_score > 0.00:
        return 'positive'
    elif nltk_score < 0.00:
        return 'negative'
    else:
        return 'neutral'

# Apply functions to text and get NLTK scoring
tweets_text_df['nltk_sent_score'] = tweets_text_df['cleaned_text'].apply(nltk_get_sent_score)

# Apply labels to score and store values in the DataFrame
tweets_text_df['nltk_label_sent'] = tweets_text_df['nltk_sent_score'].apply(nltk_label_sent)


# In[22]:


#Now need to print to check and make sure the NLTK scores have been added correctly 
print(tweets_text_df.head(10))


# In[24]:


#Now to do some examination of the vectorized data and compare to the sentiment gained from the text
#To do this will make a dataframe of the vectorization process
#vect_df = pd.DataFrame(x_count.toarray(), columns=count_vectorizer.get_feature_names_out())

#print(vect_df.head())

#Ok...well....now we see why the sparse matrix is a great idea. While I have many memory I do not have 2TB 
# worth. Turns out the vocabulary is indeed large. 


# In[25]:


#We have a couple of options for dimensionality reduction, TFIDF vectors and stemming. 
#We can try both on the data and compare the shape of the resulting df to see which is more effective. 
#It should be noted that at this point the stop_words have been applied. 
#HOWEVER, it should also be noted that the stop_words list used was taken from the NLTK package. 
#Other stop words may be more effecient with this type of text. Additionally could modify. 
#If word frequencies arent what they should be and contain https, com, imgur, etc etc then will modify

#First will use the  TFIDF vectorizer
#Initialize the vectorizer
tfidf_vectorizer = TfidfVectorizer()

#Fit and transform the text data
trans_tfidf = tfidf_vectorizer.fit_transform(tweets_text_df['cleaned_text'])

#Check shape before doign anything else
print(trans_tfidf.shape)


# In[29]:


#Hmmm....according to the shape shown here there was no reduction compared to the none vectorized 
#Import Stemmer requirements 
from nltk.stem import PorterStemmer

#Initialize the stemmer
stemmer = PorterStemmer()

#define stemming function to apply to cleaned_text of df
def das_stemmer(text):
    #tokenize text
    st_tokens = word_tokenize(text)
    #Stem the words
    stemmed_words = [stemmer.stem(word) for word in st_tokens]
    #rejoin the strings
    return ' '.join(stemmed_words)


# In[30]:


#Apply the stemming function 
tweets_text_df['stemmed_text'] = tweets_text_df['cleaned_text'].apply(das_stemmer)

#Display the head of the df to check results 
print(tweets_text_df.head(10))


# In[31]:


#Run functions on newly created stemmed text and compare with other methods 
tweets_text_df['nltk_stemmed_score'] = tweets_text_df['stemmed_text'].apply(nltk_get_sent_score)

# Apply labels to score and store values in the DataFrame
tweets_text_df['nltk_label_stemmed'] = tweets_text_df['nltk_stemmed_score'].apply(nltk_label_sent)


# In[32]:


#check NLTK scoring on stemmed words 
print(tweets_text_df.head(10))


# In[33]:


#Now to do the same with the Vader sentiment analysis, will need to reload vader sentimentinitalizer 
tweets_text_df['vdr_stemmed_score'] = tweets_text_df['stemmed_text'].apply(get_sent_score)

#And apply labels to stemmed vdr score
tweets_text_df['vdr_stemmed_lbl'] = tweets_text_df['vdr_stemmed_score'].apply(label_sent)


# In[34]:


#And check the df to make sure data was integrated correctly 
print(tweets_text_df.head(10))


# In[38]:


#Make a plot comparing the averages between each of the sentiment scores 
import seaborn as sns
import matplotlib.pyplot as plt

#Get average of each method 
avg_sent_scores = tweets_text_df[['nltk_sent_score','vdr_sentiment_score', 'nltk_stemmed_score', 'vdr_stemmed_score']].mean()

#Make data clean for plot
avg_sent_scores_df = avg_sent_scores.reset_index()
avg_sent_scores_df.columns = ['Method', 'Avg Value']

#Create a barplot using seaborn 
plt.figure(figsize=(10,6))
sns.barplot(data=avg_sent_scores_df, x='Method', y='Avg Value', palette="magma")
plt.title("Comparison of Methods via Average Sentiment Scoring")
plt.ylabel("Average Value")
plt.xlabel("Method")
plt.xticks(rotation=45)
plt.show()


# In[46]:


#Also make a plot comparing the frequencies of each method 
#pull the columns to make a new df for analysis 
sent_lbl_cols = ['nltk_label_stemmed', 'vdr_stemmed_lbl', 'vdr_sent_label', 'nltk_label_sent']
#wow really should have been more consistent with the naming 

#make loop to pull frequency of occurance for each term out of columns 
for column in sent_lbl_cols:
    #count frequency 
    label_counts = tweets_text_df[column].value_counts()
    #Convert to df
    label_counts_df = label_counts.reset_index()
    label_counts_df.columns = ['Label', 'Count']
    
    #Make a plot using seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=label_counts_df, x='Label', y='Count', hue='Label', palette='plasma')
    plt.title(f'Label Frequencies for {column}')
    plt.ylabel('Frequency')
    plt.xlabel('Sentiment Label')
    plt.tight_layout()
    plt.show()


# In[47]:


#Fit and transform the text data
trans_tfidf1 = tfidf_vectorizer.fit_transform(tweets_text_df['stemmed_text'])

#Check shape before doign anything else
print(trans_tfidf1.shape)


# In[ ]:




