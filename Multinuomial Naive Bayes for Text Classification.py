#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Program Author: Kent Roller
#Program Title: IST736 Homework 4
#Creation Date: Febuary 02 2025
#Progam purpose: Import supplied text data and prepare for machine learning task using Multinomal Naive 
# Bayes algorithim. Classification purpose of program is to identify one of two label types, either 
# under the "sentiment" label or under the "authenticity" label. The program WEKA was requested to perform 
# this assignment however this task in unknown to the author. However, will implement the same using the 
# tools available in python. Two models, one for each label will be made, and the training split will 
# be handled using 10-fold cross validation as opposed to hold-out training.*note: for the gathering 
# of the top 20 words had to fit model, used entire matrix for this purpose instead of holding observations
# out since probability calculation was the goal for this step. 


# In[1]:


import pandas as pd


# In[6]:


#Specify file path on system where text file is located
file_path = "C:/Users/super/Downloads/deception_data_converted_final.tsv"


# In[13]:


#Read in file 
mnb_df = pd.read_csv(file_path, sep="\t", encoding="utf-8")
#Print head of df to make sure file was read in correctly 
print(mnb_df.head(10))


# In[20]:


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


# In[15]:


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


# In[21]:


#Strip the punctuation and convert to lower case
def cleaner_text(text):
    #REGEX to remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    #Convert text to lower 
    text = text.lower().strip()
    return text

#Apply function to review_clean1
mnb_df['review_clean1'] = mnb_df['review_clean1'].apply(cleaner_text)


# In[22]:


#Check output to make sure it is cromulent
print(mnb_df.head(10))
#Glad I checked, accidently placed a W instead of w in the Regex statement and lets just say that 
# was definetely not the desired effect. 


# In[23]:


#Convert to sparse matrix
#Capping features to keep relevant information and drop the rest
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)

sparse_mtx=vectorizer.fit_transform(mnb_df['review_clean1'])

#Check the resulting shape of the matrix
print(sparse_mtx.shape)


# In[32]:


#I guess given the size of the data the max_features arg makes little sense....annnyway
#Need to encode the labels for use with the naive bayes model for classification
#For the lie column we can encode it as a binary option since there are 2 possible labels
#Set true output to 1 and false to 0
y_lie = mnb_df['lie'].map({'t':1, 'f':0})
#And the same for the sentiment since we have positive(p) or negative(n) 
# as the two choices
y_sent = mnb_df['sentiment'].map({'p':1, 'n': 0})


# In[35]:


from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
#Make seperate models for lie and sentiment detection 
nb_lie = MultinomialNB()
#Make model
scores = cross_val_score(nb_lie, sparse_mtx, y_lie, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {scores.mean():.4f}")


# In[37]:


#and do the same for the sentiment analysis 
nb_sent = MultinomialNB()
#Make model
scores1 = cross_val_score(nb_sent, sparse_mtx, y_sent, cv=10, scoring='accuracy')
#Print average accuracy across the 10 folds
print(f"10-Fold Cross Validation Accuracy: {scores1.mean():4f}")


# In[38]:


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


# In[41]:


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


# In[45]:


#Ok, so, turns out, cross fold discards the model and doesnt retain information
#So...need to re-run naive bayes model to fit the data otherwise cant pull words
#so, need to make a model for the lie and sentiment labels 

#naive bayes previously initialized so can call here as well
nb_lie.fit(sparse_mtx, y_lie)
#Do the same for sentiment 
nb_sent.fit(sparse_mtx, y_sent)


# In[47]:


#Ok, getting the top 20 is a little technical but will explain in the paper
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


# In[ ]:




