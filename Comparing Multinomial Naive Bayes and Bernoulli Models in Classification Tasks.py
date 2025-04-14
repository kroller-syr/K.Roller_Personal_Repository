#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Program Author: Kent Roller
#Program Title: IST736 Homework 6
#Creation Date: Febuary 17 2025
#Progam purpose: Import supplied text data and prepare for machine learning task using Multinomal Naive 
# Bayes and Bernoulli algorithms. Classification purpose of program is to identify one of two label types, either 
# under the "sentiment" label or under the "authenticity" label. 
# Four models in total, two models, one for each label and algorithm will be made, and the training split will 
# be handled using 10-fold cross validation as opposed to hold-out training. 


# In[1]:


import pandas as pd


# In[2]:


#Specify file path on system where text file is located
file_path = "C:/Users/super/Downloads/deception_data_converted_final.tsv"


# In[3]:


#Read in file 
mnb_df = pd.read_csv(file_path, sep="\t", encoding="utf-8")
#Print head of df to make sure file was read in correctly 
print(mnb_df.head(10))


# In[4]:


import re
#Remove non-ASCII characters (if any) from the dataset using re pkg and REGEX statement in a function
def clean_text(text):
    #REGEX statement for non-ASCII characters 
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return text

#Apply function to the text data
mnb_df['review_clean1'] = mnb_df['review'].apply(clean_text)

#Check to make sure data is still functional
print(mnb_df.head(10))


# In[5]:


#Import pkgs needed to perform vectorization on data
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

#Call stop words
nltk.download('punkt')
nltk.download('stopwords')

#Initialize the stopwords colleciton to english since this is the target language
stop_words = set(stopwords.words('english'))

#NOTE:This section was copied from a previous assignment(HW2) and not all components are utilized in the 
# following code


# In[6]:


#Strip the punctuation and convert to lower case
def cleaner_text(text):
    #REGEX to remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    #Convert text to lower 
    text = text.lower().strip()
    return text

#Apply function to review_clean1
mnb_df['review_clean1'] = mnb_df['review_clean1'].apply(cleaner_text)


# In[7]:


#Check output to make sure it is cromulent
print(mnb_df.head(10))
#Glad I checked, accidently placed a W instead of w in the Regex statement and lets just say that 
# was definetely not the desired effect. 


# In[8]:


#Convert to sparse matrix
#Capping features to keep relevant information and drop the rest
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)

sparse_mtx=vectorizer.fit_transform(mnb_df['review_clean1'])

#Check the resulting shape of the matrix
print(sparse_mtx.shape)


# In[9]:


#I guess given the size of the data the max_features arg makes little sense....annnyway
#Need to encode the labels for use with the naive bayes model for classification
#For the lie column we can encode it as a binary option since there are 2 possible labels
#Set true output to 1 and false to 0
y_lie = mnb_df['lie'].map({'t':1, 'f':0})
#And the same for the sentiment since we have positive(p) or negative(n) 
# as the two choices
y_sent = mnb_df['sentiment'].map({'p':1, 'n': 0})


# In[10]:


from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
#Make seperate models for lie and sentiment detection 
nb_lie = MultinomialNB()
#Make model
scores = cross_val_score(nb_lie, sparse_mtx, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {scores.mean():.4f}")


# In[11]:


#and do the same for the sentiment analysis 
nb_sent = MultinomialNB()
#Make model
scores1 = cross_val_score(nb_sent, sparse_mtx, y_sent, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {scores1.mean():4f}")


# In[12]:


#Make visualizations because they look better than a wall of code
import matplotlib.pyplot as plt
import numpy as np

#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, scores, color='crimson', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification')
plt.xticks(folds)
plt.show()


# In[13]:


#Do the same for the sentiment classification 
#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, scores1, color='blue', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification')
plt.xticks(folds)
plt.show()


# In[14]:


#Ok, so, turns out, cross fold discards the model and doesnt retain information
#So...need to re-run naive bayes model to fit the data otherwise cant pull words
#so, need to make a model for the lie and sentiment labels 

#naive bayes previously initialized so can call here as well
nb_lie.fit(sparse_mtx, y_lie)
#Do the same for sentiment 
nb_sent.fit(sparse_mtx, y_sent)


# In[15]:


#Ok, getting the top 20 requires some tinkering
#Basics are, Multinomial means we give weight to frequency counts
#IN which case to find the values we are after we can use log probablities 

#Get feature names out of vectorizer (if we want to make sense of the word)
feature_names = np.array(vectorizer.get_feature_names_out())

#Create function to get wordlist out of the feature names
def git_ma_wordz (model, feature_names, n=20):
    #Get log probablities 
    top_words_indx = np.argsort(model.feature_log_prob_[0])[-n:][::-1]
    return feature_names[top_words_indx]

#Apply function to lie classification 
words_lie = git_ma_wordz(nb_lie, feature_names)
print("Top 20 Indicative Words for Lie Classification:")
print(words_lie)

#Apply function to the sentiment classification 
words_sent = git_ma_wordz(nb_sent,feature_names)
print("Top 20 Indicative Words for Sentiment Classification")
print(words_sent)


# In[16]:


#Now need to apply Bernoulli model to the data. This means we will need to start over 
#at the step where the data has REGEX applied to it, but before vectorization. 
#Since Bernoulli algorithms depend on the presence or absence of the word versus the 
# the frequency of the word in the document, we need to use a different vectorization method for the data
#Check the og data
print(mnb_df.head())


# In[18]:


#Ok, so now we just apply the different vectorization to review_clean1 and off we go
#Hmm...CountVectorization is supposed to have a built in stop words dictionary but will use 
# the one declared above instead
from sklearn.feature_extraction.text import CountVectorizer

#Need to convert stop words from nltk to list as currently it is an object
#And the arg in CountVec requires a str as an input
stop_words = list(stopwords.words('english'))
#Initialize the count vectorizer but call stop word list declared above
vectorizer = CountVectorizer(stop_words=stop_words)
#Vectorize clean_review1
count_vec_review = vectorizer.fit_transform(mnb_df["review_clean1"])


# In[20]:


#Ok, list conversion worked
#Need to import stuff for Bernoulli 
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, classification_report, make_scorer

#Define the target variables 
y_lie_bn = mnb_df["lie"]
y_sentiment_bn = mnb_df["sentiment"]

#Intialize the Bernoullie model 
bn_model = BernoulliNB()

#perform 10 fold cross validation for lie classification 
bern_cv_score = cross_val_score(bn_model, count_vec_review, y_lie_bn, cv=10, scoring='accuracy')

#Do the same for the sentiment classification
bern_cv_sent_score = cross_val_score(bn_model, count_vec_review, y_sentiment_bn, cv=10, scoring="accuracy")

#Print the results from the model
print(f"Mean Accuracy Lie Classification: {bern_cv_score.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification: {bern_cv_sent_score.mean():4f}")


# In[22]:


#Now to make visualizations similarily to how we did for MNB cross fold validation
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_score, color='skyblue', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli)')
plt.xticks(folds)
plt.show()


# In[31]:


#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_sent_score, color='OliveDrab', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (Bernoulli)')
plt.xticks(folds)
plt.show()


# In[26]:


#Ok. Now need to do some additional stuff to make the resulting report a little more robust. 
#First, should make a visulization of the label counts, as that was not done previously. 
#Get counts for each label
lie_label_counts = mnb_df["lie"].value_counts()
sent_label_counts = mnb_df["sentiment"].value_counts()

#use matplotlib to make pie plot
labels1 = ["true", "false"]
plt.pie(lie_label_counts, labels=labels1)
plt.show


# In[30]:


labels2 = ["positive", "negative"]
colorz = ["NavajoWhite", "RebeccaPurple"]
plt.pie(sent_label_counts, labels=labels2, colors=colorz)
plt.show


# In[28]:


#ok, it appears the data set is balanced. This is probably mentioned on the assignment or download page. 


# In[35]:


#Need to create some additional models that alter some of the parameters within the models themselves
# In order to see if better performance can be obtained. 
#Need to decide on which hyper parameters to tune with each model. 
#For Bernoulli, dont need to adjust Prior Probablity as the classes are balanced. 
#Dont need to manually set class priors either for the same reason
#Binarization seems ok, so probably no need to tune that. 
#Which leaves us with changing the alpha. Default is 1. 
#We can make a couple of models that vary this. 
#Likewise, we can add to the pre processing to see if this improves performance. 

#To start, we will rerun the bernoulli but this time specifying the alpha value
#perform 10 fold cross validation for lie classification 
bn_model1 = BernoulliNB(alpha=0.01)
bern_cv_score_alpha1 = cross_val_score(bn_model1, count_vec_review, y_lie_bn, cv=10, scoring='accuracy')
bern_cv_sent_score_alpha1= cross_val_score(bn_model1, count_vec_review, y_sentiment_bn, cv=10, scoring='accuracy')

#Do the same for some other values
#And yeah, could have done this in an automated way
#But prefer having the iterations tied to a variable. Which..again, could have been automated. All the same. 
bn_model2 = BernoulliNB(alpha=0.5)
bern_cv_score_alpha2 = cross_val_score(bn_model2, count_vec_review, y_lie_bn, cv=10, scoring='accuracy')
bern_cv_sent_score_alpha2 = cross_val_score(bn_model2,count_vec_review, y_sentiment_bn, cv=10, scoring='accuracy')

bn_model3 = BernoulliNB(alpha=5.0)
bern_cv_score_alpha3 = cross_val_score(bn_model3, count_vec_review, y_lie_bn, cv=10, scoring='accuracy')
bern_cv_sent_score_alpha3 = cross_val_score(bn_model3, count_vec_review, y_sentiment_bn, cv=10, scoring='accuracy')


# In[36]:


#Make visualizations for each of the models above 

#plot for bn_model1 lie accuracy
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_score_alpha1, color='DarkSlateBlue', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (alpha=0.01)')
plt.xticks(folds)
plt.show()

#plot for bn_model1 sentiment accuracy
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_sent_score_alpha1, color='Tomato', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (Bernoulli) (alpha=0.01)')
plt.xticks(folds)
plt.show()

#plot for bn_model2 lie accuracy
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_score_alpha2, color='CornflowerBlue', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (alpah=0.5)')
plt.xticks(folds)
plt.show()


#plot for bn_model2 sentiment accuracy
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_sent_score_alpha2, color='Peru', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (Bernoulli) (alpha=0.5)')
plt.xticks(folds)
plt.show()


#plot for bn_model3 lie accuracy 
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_score_alpha3, color='DarkCyan', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (alpha=5.0)')
plt.xticks(folds)
plt.show()


#plot for bn_model3 sentiment accuracy
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, bern_cv_sent_score_alpha3, color='MediumSeaGreen', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (alpha=5.0)')
plt.xticks(folds)
plt.show()


# In[37]:


print(f"Mean Accuracy Lie Classification for alpha=0.01: {bern_cv_score_alpha1.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification for alpha=0.01: {bern_cv_sent_score_alpha1.mean():4f}")
print(f"Mean Accuracy Lie Classification for alpha=0.5: {bern_cv_score_alpha2.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification for alpha=0.5: {bern_cv_sent_score_alpha2.mean():4f}")
print(f"Mean Accuracy Lie Classification for alpha=5.0: {bern_cv_score_alpha3.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification for alpha=5.0: {bern_cv_sent_score_alpha3.mean():4f}")


# In[46]:


#Should probably make a better way to compare these
#Store the model outputs into a df
folds = list(range(1,11))

alpha_accuracy_df = pd.DataFrame({
    #List the total number of models being stores
    'Fold' : folds*8,
    #Store the model itself since the only output from the model is the scoring
    'Accuracy' : list(bern_cv_score) + list(bern_cv_sent_score) + list(bern_cv_score_alpha1) + list(bern_cv_sent_score_alpha1)
    + list(bern_cv_score_alpha2) + list(bern_cv_sent_score_alpha2) + list(bern_cv_score_alpha3) + list(bern_cv_sent_score_alpha3),
    #Add labels to the values stored in 'Accuracy'
    'Model' : (['Alpha_lie=1.0'] * 10) + (['Alpha_sent=1.0'] *10) + (['Alpha_lie=0.01']*10) +
    (['Alpha_sent=0.01']*10) + (['Alpha_lie=0.05']*10) + (['Alpha_sent=0.05']*10) + (['Alpha_lie=5.0']*10) +
    (['Alpha_sent=5.0']*10)

})

#Make a for loop to iterate through the list and generate a line based on the values
plt.figure(figsize=(10,6))
#Loop through each model stored in the new df 
for model_name in alpha_accuracy_df['Model'].unique():
    subset=alpha_accuracy_df[alpha_accuracy_df['Model']==model_name]
    plt.plot(subset['Fold'], subset['Accuracy'], marker='o', label=model_name)
#Add lavbels to plot    
plt.xlabel("Fold Number")
plt.ylabel("Accuracy")
plt.title("Comparison of Varying Alpha Values Using Bernoulli Models")
#Add legend and specif location otherwise spawns on graph
plt.legend(title="Model", bbox_to_anchor=(1.05, 1), loc='upper left')
#Grid makes it a bit more readable
plt.grid(True)
#Display plot
plt.show


# In[47]:


#Ok, now need to do some variation of the vectorization process, we will start with ngrams
#redefine vectorizer
vectorizer = CountVectorizer(ngram_range=(1,2), stop_words="english")

#Apply vectorizer to data, this time using ngram range of 1-2, meaning it will take unigrams and bigrams
count_vec_review_ngram1 = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now reapply the Bernoulli model 
#perform 10 fold cross validation for lie classification 
ngram_cv_score = cross_val_score(bn_model, count_vec_review_ngram1, y_lie_bn, cv=10, scoring='accuracy')

#Do the same for the sentiment classification
ngram_cv_sent_score = cross_val_score(bn_model, count_vec_review_ngram1, y_sentiment_bn, cv=10, scoring="accuracy")

#And now print the accuracy for the models
print(f"Mean Accuracy Lie Classification: {ngram_cv_score.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification: {ngram_cv_sent_score.mean():4f}")


# In[48]:


#now to do the same but this time only using bigrams in the model
vectorizer = CountVectorizer(ngram_range=(2,2), stop_words="english")

#Apply vectorizer to data, this time using ngram range of 2, meaning it will only take bigrams
count_vec_review_ngram2 = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now reapply the Bernoulli model 
#perform 10 fold cross validation for lie classification 
ngram_cv_score1 = cross_val_score(bn_model, count_vec_review_ngram2, y_lie_bn, cv=10, scoring='accuracy')

#Do the same for the sentiment classification
ngram_cv_sent_score1 = cross_val_score(bn_model, count_vec_review_ngram2, y_sentiment_bn, cv=10, scoring="accuracy")

#And now print the accuracy for the models
print(f"Mean Accuracy Lie Classification: {ngram_cv_score1.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification: {ngram_cv_sent_score1.mean():4f}")


# In[49]:


#Make plots for the above output
#Plot for ngram lie
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_cv_score, color='BlueViolet', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (ngram(1,2))')
plt.xticks(folds)
plt.show()

#Make a plot for ngram sent
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the sentiment model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_cv_sent_score, color='IndianRed', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (Bernoulli) (ngram(1,2))')
plt.xticks(folds)
plt.show()

#make a plot for ngram lie 2
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_cv_score1, color='CadetBlue', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (Bernoulli) (ngram(2,2))')
plt.xticks(folds)
plt.show()

#Make a plot for ngram sentiment 2
#Declare number of folds
folds= np.arange(1,11)

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_cv_sent_score1, color='SaddleBrown', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (Bernoulli) (ngram(2,2))')
plt.xticks(folds)
plt.show()


# In[52]:


#Now peform redo tfidf vectorization but using ngrams this time as well 
vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')

#Apply vectorizer to data
ngram_tfidf1 = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now apply Multinomial Naive Bayes to the data
mnb = MultinomialNB()
#Make model
ngram_mnb_lie = cross_val_score(mnb, ngram_tfidf1, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_lie.mean():.4f}")

#And do the same for sentiment
ngram_mnb_sent = cross_val_score(mnb, ngram_tfidf1, y_sent, cv=10, scoring='accuracy')
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_sent.mean():4f}")


# In[54]:


#Plot time
#plot for ngram_mnb_lie
#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_mnb_lie, color='#265226', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (MNB) (ngram(1,2))')
plt.xticks(folds)
plt.show()

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_mnb_sent, color='#0e5850', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (MNB) (ngram(1,2))')
plt.xticks(folds)
plt.show()


# In[56]:


#Now peform redo tfidf vectorization but using ngrams this time as well 
vectorizer = TfidfVectorizer(ngram_range=(1,3), stop_words='english')

#Apply vectorizer to data
ngram_tfidf2 = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now apply Multinomial Naive Bayes to the data
mnb = MultinomialNB()
#Make model
ngram_mnb_lie1 = cross_val_score(mnb, ngram_tfidf2, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_lie1.mean():.4f}")

#And do the same for sentiment
ngram_mnb_sent1 = cross_val_score(mnb, ngram_tfidf2, y_sent, cv=10, scoring='accuracy')
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_sent1.mean():4f}")


# In[57]:


#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_mnb_lie, color='#801acc', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Lie Classification (MNB) (ngram(1,3))')
plt.xticks(folds)
plt.show()

#Make a plot of the lie model accuracy for each fold 
plt.figure(figsize=(10,5))
plt.bar(folds, ngram_mnb_sent, color='#8c731a', alpha=0.7)
#add labels to the plt
plt.xlabel('Fold Number')
plt.ylabel('Accuracy')
plt.title('10-Fold Cross Validation Accuracy for Sentiment Classification (MNB) (ngram(1,3))')
plt.xticks(folds)
plt.show()


# In[58]:


#Now peform redo tfidf vectorization but using ngrams this time as well 
vectorizer = TfidfVectorizer(ngram_range=(2,2), stop_words='english')

#Apply vectorizer to data
ngram_tfidf3 = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now apply Multinomial Naive Bayes to the data
mnb = MultinomialNB()
#Make model
ngram_mnb_lie2 = cross_val_score(mnb, ngram_tfidf3, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_lie2.mean():.4f}")

#And do the same for sentiment
ngram_mnb_sent2 = cross_val_score(mnb, ngram_tfidf3, y_sent, cv=10, scoring='accuracy')
print(f"10-Fold Cross Validation Accuracy: {ngram_mnb_sent2.mean():4f}")


# In[59]:


#one last model with no stop words applied using the defaults of the vectorizer 
vectorizer = TfidfVectorizer()

#Apply vectorizer to data
base_tfidf = vectorizer.fit_transform(mnb_df['review_clean1'])

#Now apply Multinomial Naive Bayes to the data
mnb = MultinomialNB()
#Make model
base_tfidf_lie = cross_val_score(mnb, base_tfidf, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {base_tfidf_lie.mean():.4f}")

#And do the same for sentiment
base_tfidf_sent = cross_val_score(mnb, base_tfidf, y_sent, cv=10, scoring='accuracy')
print(f"10-Fold Cross Validation Accuracy: {base_tfidf_sent.mean():4f}")


# In[60]:


#Do the same with the Bernoulli model 
vectorizer = CountVectorizer()
#Vectorize clean_review1
count_vec_review = vectorizer.fit_transform(mnb_df["review_clean1"])

bn_model = BernoulliNB()

#perform 10 fold cross validation for lie classification 
bern_base_lie = cross_val_score(bn_model, count_vec_review, y_lie_bn, cv=10, scoring='accuracy')

#Do the same for the sentiment classification
bern_base_sent = cross_val_score(bn_model, count_vec_review, y_sentiment_bn, cv=10, scoring="accuracy")

#Print the results from the model
print(f"Mean Accuracy Lie Classification: {bern_base_lie.mean():.4f}")
print(f"Mean Accuracy Sentiment Classification: {bern_base_sent.mean():4f}")


# In[65]:


#I Lied, now lastly, going to add to the stopwords list to see if that affects the outcome of the base model
stop_words=set(stopwords.words('english'))
#add 5 words from the top 20 words list generated earlier
top_cut = {"went", "want", "friends", "just", "came", "come"}
#update the stop words list
stop_words.update(top_cut)
#...yeah its sloppy, sorry. but hey, it works?
stop_words = list(stopwords.words('english'))

#Now use the stop words in the vectorizers
vectorizer = CountVectorizer(stop_words=stop_words)

#use the vectorizer on the data
stp_cnt_vc = vectorizer.fit_transform(mnb_df['review_clean1'])

#intilialize model
bn2_elctbglo = BernoulliNB()

#apply model to data
lie_stp_mdf_bn = cross_val_score(bn2_elctbglo, stp_cnt_vc, y_lie_bn, cv=10, scoring='accuracy')
#and sent
sent_stp_mdf_bn = cross_val_score(bn2_elctbglo, stp_cnt_vc, y_sentiment_bn, cv=10, scoring='accuracy')

#Print accuracy
print(f"Mean Accuracy Lie Classification: {lie_stp_mdf_bn.mean():.4f}")
print(f"Mean Accuracy Sent Classification: {sent_stp_mdf_bn.mean():.4f}")


# In[66]:


#Intialize other vectorizer. 
#and yeah, i should probably just store the vectorizer in a unique variable so I wouldnt have to call it 
# 1000 times but I havent. I dont have a reason I just havent. I need to. 
vectorizer = TfidfVectorizer(stop_words=stop_words)

#use vectorizer on data for mnb
stp_mdf_tfdf = vectorizer.fit_transform(mnb_df["review_clean1"])

#Intialize model
mnb2_elctbglo = MultinomialNB()

#Fit model to data
lie_mnb_stpwd = cross_val_score(mnb2_elctbglo, stp_mdf_tfdf, y_lie, cv=10, scoring='accuracy')
#and for the sent
sent_mnb_stpwd = cross_val_score(mnb2_elctbglo, stp_mdf_tfdf, y_sent, cv=10, scoring='accuracy')

#And then print the resulting accuracy
print(f"Mean Accuracy Lie Classification: {lie_mnb_stpwd.mean():.4f}")
print(f"Mean Accuracy Sent Classification: {sent_mnb_stpwd.mean():.4f}")


# In[ ]:




