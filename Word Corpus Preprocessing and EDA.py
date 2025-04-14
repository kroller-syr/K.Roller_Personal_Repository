#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Project Name: IST736 Homework 3
#Author: Kent Roller
#Creation Date: Jan 28 2025
#Project Purpose: To import a corpus file and then perform text pre-processing and ready the text 
# for machine learning algorithims by performing task such as vectorizing the text and embedding the text


# In[14]:


#Read in the corpus document, a collection of SMS text messages which should be prelabeled 
file_path = "C:/Users/super/OneDrive/Desktop/SMSSpamCollection"

#open the file path and read file
with open (file_path, 'r', encoding='utf-8') as file:
    sms_corpus = file.read()

#print first 500 characters to make sure corpus was imported correctly 
print(sms_corpus[:500])


# In[ ]:





# In[15]:


#Ok.....so, it looks like to make use of the labels in the data the data must be converted to a df?
#My understanding may not be complete, but from what I can gather, each observation contains both the label
#and the message. To be able to split the data by label we must set this to a df where the label is seperate
#from the observation. The label and the message appear to be tab delimited which means we should be able
#to use the the white space as the thing that seperates them and put them into df format.
#Of course then the question becomes, if I convert it to a df am I satisfying the requiremnts for the 
#assignment. Hmmnm....the instructions state to vectorize the corpus. So...
#I guess we can try to vectorize first and then split based on label after vectorization? 


# In[16]:


#Okay, after some more reading it looks like I can split the corpus when reading it in to prevent the labels
#from being vectorized with the message itself. So we will try this method to comply with instructions in 
#assignment 
#Read the file in but split on read 
#Initialize variables for messages and lables
labels=[]
messages=[]

with open (file_path, 'r', encoding='utf-8') as file:
    for line in file:
        #Split the message between label and text
        parts = line.strip().split(maxsplit=1)
        #Define the rules for when the split occurs
        if len(parts) == 2:
            labels.append(parts[0])
            messages.append(parts[1])


# In[17]:


#Now to try and vectorize the message text 
from sklearn.feature_extraction.text import TfidfVectorizer
#Call Tfidf
vectorizer0 = TfidfVectorizer()
#Apply vectorizer to the messages text, leaving the label text raw
x = vectorizer0.fit_transform(messages) 


# In[18]:


import pandas as pd
#Now that message text is vectorized can port to df for comparison between labels and word frequency
x_dense = x.toarray()

#Create vectorized df
vectorized_df = pd.DataFrame(x_dense)
vectorized_df['label'] = labels

#See if it worked
print(vectorized_df.head(10))


# In[19]:


#Without any type of pre processing and just performing TfIdf vectorization on the raw message data results
# in a df with 8714 columns x total message count
#This can be compared to removing the punctuation first and then vectorizing the data
import re
from sklearn.feature_extraction.text import CountVectorizer
#Make function to remove punctaution 
def remove_punct(text):
    #Use regex statement to remove the punctuation
    return re.sub(r'[^\w\s]', '', text)

#Apply regex function to messages variable from previous step
punctless_messages = [remove_punct(message) for message in messages]

#use tdidf to compare to previous step
#also use count vectorizer to perform analysis on the vectorized data
vectorizer1 = TfidfVectorizer()
#Apply vectorizer to the messages text, leaving the label text raw
x_punctless_tfidf = vectorizer1.fit_transform(punctless_messages) 

x_dense2 = x_punctless_tfidf.toarray()

#Create vectorized df of punctless vectorization
vectorized_punctless_tfidf = pd.DataFrame(x_dense2)
vectorized_punctless_tfidf['label'] = labels

#See if it worked
print(vectorized_punctless_tfidf.head(10))


# In[20]:


#Huh....Thats, unexpected. The number of columns has increased compared to the version of the 
# messages with the punctuation retained. One would think removing the punctuation would lower the number
# of columns, though, what appears to be the case is that perhaps multiple words were being encapsulated
# with the punctuation, which registered multiple words as the same word starting with same punctuation.

#Now use count vectorizer instead of tdidf vectorizer 
from sklearn.feature_extraction.text import CountVectorizer
vectorizer2 = CountVectorizer()
x_punctless_countvec = vectorizer2.fit_transform(punctless_messages)

#place count vectors into array
x_dense_3 = x_punctless_countvec.toarray()

#Place into dataframe
vectorized_punctless_countvec= pd.DataFrame(x_dense_3)
#Add labels
vectorized_punctless_countvec['labels'] = labels

#Check to make sure it worked
print(vectorized_punctless_countvec.head(10))


# In[21]:


#Now need to get word frequencies between groups to compare methods of vectorization
#pull feature names out of data
feature_names_counvec = vectorizer2.get_feature_names_out()
#Assign feature names to df. This is needed as otherwise feature names(words) can get lost and 
# word list will be represented by integers, not very useful unless you knew the mapping by heart 
vectorized_punctless_countvec = pd.DataFrame(x_dense_3, columns=feature_names_counvec)
vectorized_punctless_countvec['labels'] = labels
#will split data to simplify count process
count_vec_ham_df = vectorized_punctless_countvec[vectorized_punctless_countvec['labels']=='ham'].drop(columns=['labels'])
count_vec_spam_df = vectorized_punctless_countvec[vectorized_punctless_countvec['labels']=='spam'].drop(columns=['labels'])

#Get the sum of occurance for each word across each of the messages per label
count_vec_ham_word_counts = count_vec_ham_df.sum().sort_values(ascending=False)
count_vec_spam_word_counts = count_vec_spam_df.sum().sort_values(ascending=False)

#Pull the top 10 words from the count variables made above
top_10_countvec_ham = count_vec_ham_word_counts.head(10)
top_10_countvec_spam = count_vec_spam_word_counts.head(10)

#Print results to see what the words are 
print("Top 10 words countvec ham messages:\n", top_10_countvec_ham)
print("Top 10 words countvec spam messages:\n", top_10_countvec_spam)


# In[22]:


#!pip install wordcloud
#!pip install pillow
#!pip install --upgrade pillow
#Make word cloud for more expanded comparison
#!pip install stylecloud
#.......evidently I just needed to reset the kernel. 
import PIL
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# In[23]:


import matplotlib.font_manager as fm
#Convert frequencies to dict
ham_countvec_freq = count_vec_ham_word_counts.to_dict()
spam_countvec_freq = count_vec_spam_word_counts.to_dict()

#Generate wordclouds, make sure to pass arg to call font_type to ensure TrueType font is used
wordcloud_countvec_ham = WordCloud(width=800, height = 400, background_color='white')    .generate_from_frequencies(ham_countvec_freq)
wordcloud_countvec_spam = WordCloud(width=800, height=400, background_color='black', colormap='Reds')    .generate_from_frequencies(spam_countvec_freq)

#Make pltfigure to put wordclouds side by side
plt.figure(figsize=(14,6))

#Ham message wordcloud
#using subplot to declare positioning of wordcloud in plt.figure made above
plt.subplot(1,2,1)
#call image
plt.imshow(wordcloud_countvec_ham,interpolation="bilinear")
#Make sure axis is not present in plot
plt.axis("off")
#add title to plot
plt.title("Ham Message WordCloud")

#Spam message wordcloud
#Same as before, declare position to make sure the plots dont overlap
plt.subplot(1,2,2)
#call spam wordcloud
plt.imshow(wordcloud_countvec_spam,interpolation="bilinear")
#Turn axis off
plt.axis('off')
plt.title('Spam Messages WordCloud')

#Print the plot
plt.show()


# In[26]:


#Ok, now to do the same with the Tfidf vectorization method. I mean, in theory, should see 
# pretty similar counts as they are just counting frequency to start with. Nonetheless, comparison awaits

#Need to call tfidf vectorizer to make sure its the one being implemented

#Now need to get word frequencies between groups to compare methods of vectorization
#pull feature names out of data
feature_names_tfidf = vectorizer1.get_feature_names_out()
#Assign feature names to df. Make sure to specify x_dense_2 here since this is the variable storing output 
#from the tfidf vectorization 
vectorized_punctless_tfidf = pd.DataFrame(x_dense2, columns=feature_names_tfidf)
vectorized_punctless_tfidf['labels'] = labels
#will split data to simplify count process
tfidf_ham_df = vectorized_punctless_tfidf[vectorized_punctless_tfidf['labels']=='ham'].drop(columns=['labels'])
tfidf_spam_df = vectorized_punctless_tfidf[vectorized_punctless_tfidf['labels']=='spam'].drop(columns=['labels'])

#Get the sum of occurance for each word across each of the messages per label
tfidf_ham_word_counts = tfidf_ham_df.sum().sort_values(ascending=False)
tfidf_spam_word_counts = tfidf_spam_df.sum().sort_values(ascending=False)

#Pull the top 10 words from the count variables made above
top_10_tfidf_ham = tfidf_ham_word_counts.head(10)
top_10_tfidf_spam = tfidf_spam_word_counts.head(10)

#Print results to see what the words are 
print("Top 10 words tfidf ham messages:\n", top_10_tfidf_ham)
print("Top 10 words tfidf spam messages:\n", top_10_tfidf_spam)


# In[27]:


ham_tfidf_freq = tfidf_ham_word_counts.to_dict()
spam_tfidf_freq = tfidf_spam_word_counts.to_dict()

#Generate wordclouds, make sure to pass arg to call font_type to ensure TrueType font is used
wordcloud_tfidf_ham = WordCloud(width=800, height = 400, background_color='white')    .generate_from_frequencies(ham_tfidf_freq)
wordcloud_tfidf_spam = WordCloud(width=800, height=400, background_color='black', colormap='Reds')    .generate_from_frequencies(spam_tfidf_freq)

#Make pltfigure to put wordclouds side by side
plt.figure(figsize=(14,6))

#Ham message wordcloud
#using subplot to declare positioning of wordcloud in plt.figure made above
plt.subplot(1,2,1)
#call image
plt.imshow(wordcloud_tfidf_ham,interpolation="bilinear")
#Make sure axis is not present in plot
plt.axis("off")
#add title to plot
plt.title("Ham tfidf Message WordCloud")

#Spam message wordcloud
#Same as before, declare position to make sure the plots dont overlap
plt.subplot(1,2,2)
#call spam wordcloud
plt.imshow(wordcloud_tfidf_spam,interpolation="bilinear")
#Turn axis off
plt.axis('off')
plt.title('Spam tfidf Messages WordCloud')

#Print the plot
plt.show()


# In[ ]:




