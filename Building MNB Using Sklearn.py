#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Program Name: IST736 Homework 7
#Program Author: Kent Roller, Async Material
#Program Purpose: Meet requirements set forth in instructions for HW7
#Program Creation Date: Febraury 28, 2025

#NOTE: The instructions say to "revise the instructors given script", I assumed this was the script mentioned
# which is why it is being used as the base of the assignment. 


# # Tutorial - build MNB with sklearn

# This tutorial demonstrates how to use the Sci-kit Learn (sklearn) package to build Multinomial Naive Bayes model, rank features, and use the model for prediction. 
# 
# The data from the Kaggle Sentiment Analysis on Movie Review Competition are used in this tutorial. Check out the details of the data and the competition on Kaggle.
# https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews
# 
# The tutorial also includes sample code to prepare your prediction result for submission to Kaggle. Although the competition is over, you can still submit your prediction to get an evaluation score.

# # Step 1: Read in data

# In[4]:


# read in the training data

# the data set includes four columns: PhraseId, SentenceId, Phrase, Sentiment
# In this data set a sentence is further split into phrases 
# in order to build a sentiment classification model
# that can not only predict sentiment of sentences but also shorter phrases

# A data example:
# PhraseId SentenceId Phrase Sentiment
# 1 1 A series of escapades demonstrating the adage that what is good for the goose is also good for the gander , some of which occasionally amuses but none of which amounts to much of a story .1

# the Phrase column includes the training examples
# the Sentiment column includes the training labels
# "0" for very negative
# "1" for negative
# "2" for neutral
# "3" for positive
# "4" for very positive

import numpy as np
import pandas as p
train=p.read_csv("C:/Users/super/OneDrive/Desktop/train.tsv", delimiter='\t')
y=train['Sentiment'].values
X=train['Phrase'].values
#Modified file path to read in file from local machine


# # Step 2: Split train/test data for hold-out test

# In[5]:


# check the sklearn documentation for train_test_split
# http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
# "test_size" : float, int, None, optional
# If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split. 
# If int, represents the absolute number of test samples. 
# If None, the value is set to the complement of the train size. 
# By default, the value is set to 0.25. The default will change in version 0.21. It will remain 0.25 only if train_size is unspecified, otherwise it will complement the specified train_size.    

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
print(X_train[0])
print(y_train[0])
print(X_test[0])
print(y_test[0])


# Sample output from the code above:
# 
# (93636,) (93636,) (62424,) (62424,)
# almost in a class with that of Wilde
# 3
# escape movie
# 2

# # Step 2.1 Data Checking

# In[6]:


# Check how many training examples in each category
# this is important to see whether the data set is balanced or skewed

unique, counts = np.unique(y_train, return_counts=True)
print(np.asarray((unique, counts)))


# The sample output shows that the data set is skewed with 47718/93636=51% "neutral" examples. All other categories are smaller.
# 
# {0, 1, 2, 3, 4}
# [[    0  4141]
#  [    1 16449]
#  [    2 47718]
#  [    3 19859]
#  [    4  5469]]

# # Exercise A

# In[15]:


# Print out the category distribution in the test data set. 
#Is the test data set's category distribution similar to the training data set's?

# Your code starts here
#Import test data
test=p.read_csv("C:/Users/super/OneDrive/Desktop/test.tsv", delimiter='\t')
#Apply labels to data
y_test=train['Sentiment'].values
X_test=train['Phrase'].values

#Set up test and train split at the same 60/40 the training data was split
X_test_train, X_test_test, y_test_train, y_test_test = train_test_split(X_test_train, y_test_train, test_size=0.4, random_state=0)

#get the shape of the arrays
print(X_test_train.shape, y_test_train.shape, X_test_test.shape, y_test_test.shape)
print(X_test_train[0])
print(y_test_train[0])
print(X_test_test[0])
print(y_test_test[0])

#Show the unique counts for each label in the test data
unique1, counts1 = np.unique(y_test_train, return_counts=True)
print(np.asarray((unique1, counts1)))


# Your code ends here


# # Step 3: Vectorization

# In[11]:


# sklearn contains two vectorizers

# CountVectorizer can give you Boolean or TF vectors
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

# TfidfVectorizer can give you TF or TFIDF vectors
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

# Read the sklearn documentation to understand all vectorization options

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# several commonly used vectorizer setting

#  unigram boolean vectorizer, set minimum document frequency to 5
unigram_bool_vectorizer = CountVectorizer(encoding='latin-1', binary=True, min_df=5, stop_words='english')

#  unigram term frequency vectorizer, set minimum document frequency to 5
unigram_count_vectorizer = CountVectorizer(encoding='latin-1', binary=False, min_df=5, stop_words='english')

#  unigram and bigram term frequency vectorizer, set minimum document frequency to 5
gram12_count_vectorizer = CountVectorizer(encoding='latin-1', ngram_range=(1,2), min_df=5, stop_words='english')

#  unigram tfidf vectorizer, set minimum document frequency to 5
unigram_tfidf_vectorizer = TfidfVectorizer(encoding='latin-1', use_idf=True, min_df=5, stop_words='english')


# ## Step 3.1: Vectorize the training data

# In[12]:


# The vectorizer can do "fit" and "transform"
# fit is a process to collect unique tokens into the vocabulary
# transform is a process to convert each document to vector based on the vocabulary
# These two processes can be done together using fit_transform(), or used individually: fit() or transform()

# fit vocabulary in training documents and transform the training documents into vectors
X_train_vec = unigram_count_vectorizer.fit_transform(X_train)

# check the content of a document vector
print(X_train_vec.shape)
print(X_train_vec[0].toarray())

# check the size of the constructed vocabulary
print(len(unigram_count_vectorizer.vocabulary_))

# print out the first 10 items in the vocabulary
print(list(unigram_count_vectorizer.vocabulary_.items())[:10])

# check word index in vocabulary
print(unigram_count_vectorizer.vocabulary_.get('imaginative'))


# Sample output:
# 
# (93636, 11967)
# [[0 0 0 ..., 0 0 0]]
# 11967
# [('imaginative', 5224), ('tom', 10809), ('smiling', 9708), ('easy', 3310), ('diversity', 3060), ('impossibly', 5279), ('buy', 1458), ('sentiments', 9305), ('households', 5095), ('deteriorates', 2843)]
# 5224

# ## Step 3.2: Vectorize the test data

# In[13]:


# use the vocabulary constructed from the training data to vectorize the test data. 
# Therefore, use "transform" only, not "fit_transform", 
# otherwise "fit" would generate a new vocabulary from the test data

X_test_vec = unigram_count_vectorizer.transform(X_test)

# print out #examples and #features in the test set
print(X_test_vec.shape)


# Sample output:
# 
# (62424, 14324)

# # Exercise B

# In[16]:


# In the above sample code, the term-frequency vectors were generated for training and test data.

# Some people argue that 
# because the MultinomialNB algorithm is based on word frequency, 
# we should not use boolean representation for MultinomialNB.
# While in theory it is true, you might see people use boolean representation for MultinomialNB
# especially when the chosen tool, e.g. Weka, does not provide the BernoulliNB algorithm.

# sklearn does provide both MultinomialNB and BernoulliNB algorithms.
# http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html
# You will practice that later

# In this exercise you will vectorize the training and test data using boolean representation
# You can decide on other options like ngrams, stopwords, etc.

# Your code starts here
#Boolean vectorizer was already used above under unigram_bool_vectorizer variable name
#as such can just call this to perform the requested action
unigram_bool_vectorizer = CountVectorizer(encoding='latin-1', binary=True, min_df=5, stop_words='english')

#Then reuse other code for vectorization
#Call the bool vectorizer instead of the non bool
X_train_vec_bool = unigram_bool_vectorizer.fit_transform(X_train)

# check the content of a document vector
print(X_train_vec_bool.shape)
print(X_train_vec_bool[0].toarray())

# check the size of the constructed vocabulary
print(len(unigram_bool_vectorizer.vocabulary_))

# print out the first 10 items in the vocabulary
print(list(unigram_bool_vectorizer.vocabulary_.items())[:10])

# check word index in vocabulary
print(unigram_bool_vectorizer.vocabulary_.get('imaginative'))

#And dont forget the test data
x_test_train_bool = unigram_bool_vectorizer.transform(X_test_train)

# print out #examples and #features in the test set
print(x_test_train_bool.shape)
# Your code ends here


# # Step 4: Train a MNB classifier

# In[105]:


# import the MNB module
from sklearn.naive_bayes import MultinomialNB

# initialize the MNB model
nb_clf= MultinomialNB()

# use the training data to train the MNB model, calling the correct vectorizer
nb_clf.fit(X_train_vec,y_train)


# # Step 4.1 Interpret a trained MNB model

# In[106]:


## interpreting naive Bayes models
## by consulting the sklearn documentation you can also find out feature_log_prob_, 
## which are the conditional probabilities
## http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html

# the code below will print out the conditional prob of the word "worthless" in each category
# sample output
# -8.98942647599 -> logP('worthless'|very negative')
# -11.1864401922 -> logP('worthless'|negative')
# -12.3637684625 -> logP('worthless'|neutral')
# -11.9886066961 -> logP('worthless'|positive')
# -11.0504454621 -> logP('worthless'|very positive')
# the above output means the word feature "worthless" is indicating "very negative" 
# because P('worthless'|very negative) is the greatest among all conditional probs

unigram_count_vectorizer.vocabulary_.get('worthless')
for i in range(0,5):
  print(nb_clf.feature_log_prob_[i][unigram_count_vectorizer.vocabulary_.get('worthless')])


# Sample output:
# 
# -8.5389826392
# -10.6436375867
# -11.8419845779
# -11.4778370023
# -10.6297551464

# In[107]:


# sort the conditional probability for category 0 "very negative"
# print the words with highest conditional probs
# these can be words popular in the "very negative" category alone, or words popular in all cateogires

#updated code to use get_feature_names_out() as previously used method has been depracated
feature_ranks = sorted(zip(nb_clf.feature_log_prob_[0], unigram_count_vectorizer.get_feature_names_out()))
very_negative_features = feature_ranks[-10:]
print(very_negative_features)


# In[108]:


#Do the same thing as above but this time for the very positive catgory (most positive category)
feature_ranks = sorted(zip(nb_clf.feature_log_prob_[4], unigram_count_vectorizer.get_feature_names_out()))
#Counter intuitively the index remains at -10 because these are the observations which have the highest
# probability, so this is not related to positive or negative connotation. 
very_positive_features = feature_ranks[-10:]
print(very_positive_features)


# # Exercise C

# In[21]:


# calculate log ratio of conditional probs

# In this exercise you will calculate the log ratio 
# between conditional probs in the "very negative" category
# and conditional probs in the "very positive" category,
# and then sort and print out the top and bottom 10 words

# the conditional probs for the "very negative" category is stored in nb_clf.feature_log_prob_[0]
# the conditional probs for the "very positive" category is stored in nb_clf.feature_log_prob_[4]

# You can consult with similar code in week 4's sample script on feature weighting
# Note that in sklearn's MultinomialNB the conditional probs have been converted to log values.

# Your code starts here

# Your code ends here


# Sample output for print(log_ratios[0])
# 
# -0.838009538739

# # Step 5: Test the MNB classifier

# In[109]:


# test the classifier on the test data set, print accuracy score

nb_clf.score(X_test_vec,y_test)


# In[24]:


# print confusion matrix (row: ground truth; col: prediction)

from sklearn.metrics import confusion_matrix
y_pred = nb_clf.fit(X_train_vec, y_train).predict(X_test_vec)
cm=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm)


# In[25]:


# print classification report

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
print(precision_score(y_test, y_pred, average=None))
print(recall_score(y_test, y_pred, average=None))

from sklearn.metrics import classification_report
target_names = ['0','1','2','3','4']
print(classification_report(y_test, y_pred, target_names=target_names))


# # Step 5.1 Interpret the prediction result

# In[26]:


## find the calculated posterior probability
posterior_probs = nb_clf.predict_proba(X_test_vec)

## find the posterior probabilities for the first test example
print(posterior_probs[0])

# find the category prediction for the first test example
y_pred = nb_clf.predict(X_test_vec)
print(y_pred[0])

# check the actual label for the first test example
print(y_test[0])


# sample output array([ 0.06434628  0.34275846  0.50433091  0.07276319  0.01580115]
# 
# Because the posterior probability for category 2 (neutral) is the greatest, 0.50, the prediction should be "2". Because the actual label is also "2", this is a correct prediction
# 

# # Step 5.2 Error Analysis

# In[27]:


# print out specific type of error for further analysis

# print out the very positive examples that are mistakenly predicted as negative
# according to the confusion matrix, there should be 53 such examples
# note if you use a different vectorizer option, your result might be different

err_cnt = 0
for i in range(0, len(y_test)):
    if(y_test[i]==4 and y_pred[i]==1):
        print(X_test[i])
        err_cnt = err_cnt+1
print("errors:", err_cnt)


# # Exercise D

# In[27]:


# Can you find linguistic patterns in the above errors? 
# What kind of very positive examples were mistakenly predicted as negative?

# Can you write code to print out the errors that very negative examples were mistakenly predicted as very positive?
# Can you find lingustic patterns for this kind of errors?
# Based on the above error analysis, what suggestions would you give to improve the current model?

# Your code starts here

# Your code ends here


# # Step 6: write the prediction output to file

# In[28]:


y_pred=nb_clf.predict(X_test_vec)
output = open('/Users/byu/Desktop/data/prediction_output.csv', 'w')
for x, value in enumerate(y_pred):
  output.write(str(value) + '\n') 
output.close()


# # Step 6.1 Prepare submission to Kaggle sentiment classification competition

# In[29]:


########## submit to Kaggle submission

# we are still using the model trained on 60% of the training data
# you can re-train the model on the entire data set 
#   and use the new model to predict the Kaggle test data
# below is sample code for using a trained model to predict Kaggle test data 
#    and format the prediction output for Kaggle submission

# read in the test data
kaggle_test=p.read_csv("/Users/byu/Desktop/data/kaggle/test.tsv", delimiter='\t') 

# preserve the id column of the test examples
kaggle_ids=kaggle_test['PhraseId'].values

# read in the text content of the examples
kaggle_X_test=kaggle_test['Phrase'].values

# vectorize the test examples using the vocabulary fitted from the 60% training data
kaggle_X_test_vec=unigram_count_vectorizer.transform(kaggle_X_test)

# predict using the NB classifier that we built
kaggle_pred=nb_clf.fit(X_train_vec, y_train).predict(kaggle_X_test_vec)

# combine the test example ids with their predictions
kaggle_submission=zip(kaggle_ids, kaggle_pred)

# prepare output file
outf=open('/Users/byu/Desktop/data/kaggle/kaggle_submission.csv', 'w')

# write header
outf.write('PhraseId,Sentiment\n')

# write predictions with ids to the output file
for x, value in enumerate(kaggle_submission): outf.write(str(value[0]) + ',' + str(value[1]) + '\n')

# close the output file
outf.close()


# # Exercise E

# In[ ]:


# generate your Kaggle submissions with boolean representation and TF representation
# submit to Kaggle
# report your scores here
# which model gave better performance in the hold-out test
# which model gave better performance in the Kaggle test


# Sample output:
# 
# (93636, 9968)
# [[0 0 0 ..., 0 0 0]]
# 9968
# [('disloc', 2484), ('surgeon', 8554), ('camaraderi', 1341), ('sketchiest', 7943), ('dedic', 2244), ('impud', 4376), ('adopt', 245), ('worker', 9850), ('buy', 1298), ('systemat', 8623)]
# 245

# # BernoulliNB

# In[30]:


from sklearn.naive_bayes import BernoulliNB
X_train_vec_bool = unigram_bool_vectorizer.fit_transform(X_train)
bernoulliNB_clf = BernoulliNB(X_train_vec_bool, y_train)


# # Cross Validation

# In[31]:


# cross validation

from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
nb_clf_pipe = Pipeline([('vect', CountVectorizer(encoding='latin-1', binary=False)),('nb', MultinomialNB())])
scores = cross_val_score(nb_clf_pipe, X, y, cv=3)
avg=sum(scores)/len(scores)
print(avg)


# # Exercise F

# In[33]:


# run 3-fold cross validation to compare the performance of 
# (1) BernoulliNB (2) MultinomialNB with TF vectors (3) MultinomialNB with boolean vectors

# Your code starts here


# Your code ends here


# # Optional: use external linguistic resources such as stemmer

# In[204]:


from sklearn.feature_extraction.text import CountVectorizer
import nltk.stem

english_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([english_stemmer.stem(w) for w in analyzer(doc)])

stem_vectorizer = StemmedCountVectorizer(min_df=3, analyzer="word")
X_train_stem_vec = stem_vectorizer.fit_transform(X_train)


# In[194]:


# check the content of a document vector
print(X_train_stem_vec.shape)
print(X_train_stem_vec[0].toarray())

# check the size of the constructed vocabulary
print(len(stem_vectorizer.vocabulary_))

# print out the first 10 items in the vocabulary
print(list(stem_vectorizer.vocabulary_.items())[:10])

# check word index in vocabulary
print(stem_vectorizer.vocabulary_.get('adopt'))


# In[34]:


#Now need to make unigram SVM model and compare the output to the MNB model made above 
#Run variation of SVC to handle sparse matrix output by vectorizer
from sklearn.svm import LinearSVC

# initialize the MNB model using LinearSVC instead of Base SVC (crashed after ~30 min runtime)
#Do not currently have RAPIDS or similar solution installed to utilize GPU, times like this 
# make me wish I had done so. 
svm_clf= LinearSVC(dual=False)

# use the training data to train the MNB model
svm_clf.fit(X_train_vec,y_train)
#Oh wow that was like 10 seconds....
#Need to make note of this because I feel like I have had similar issues with SVM before for the same reason


# In[36]:


#Get feature ranks for very positive words in the SVM model 
#Method varies slightly as SVM does not have same retrieval option as MNB
# Get feature names from CountVectorizer
feature_names = unigram_count_vectorizer.get_feature_names_out()

# Extract SVM coefficients 
#NOTE: Because of the way LinearSVC works, the coeffiecients are already in a numpy array, so 
# trying to use the same code as for the MNB wont work. 
feature_weights = svm_clf.coef_.ravel()  

# Pair feature names with their corresponding weights
feature_ranks = sorted(zip(feature_weights, feature_names))

# Get the 10 most positive features 
very_positive_features = feature_ranks[:10]  

print(very_positive_features)


# In[38]:


#And print the 10 most negative words for the SVM unigram model
very_negative_features = feature_ranks[-10:]
print(very_negative_features)


# In[45]:


#Print accuracy for svm model
svm_clf.score(X_test_vec,y_test)


# In[46]:


#Make and print confusion matrix for SVM model
y_pred = svm_clf.fit(X_train_vec, y_train).predict(X_test_vec)
cm1=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm1)


# In[42]:


#Print out report for precision and F1 score for SVM model
print(precision_score(y_test, y_pred, average=None))
print(recall_score(y_test, y_pred, average=None))

target_names = ['0','1','2','3','4']
print(classification_report(y_test, y_pred, target_names=target_names))


# In[49]:


#Build the models again but this time using the vectorizer containing both unigrams and bigrams
#for comparison against unigram only model
#  unigram boolean vectorizer, set minimum document frequency to 5, set ngram_range to include unigram and bigram
unigram_bool_vectorizer2 = CountVectorizer(encoding='latin-1', binary=True, min_df=5, ngram_range=(1,2), stop_words='english')


# In[50]:


#Use the vectorizer on the data
X_train_vec_bool = unigram_bool_vectorizer2.fit_transform(X_train)

# check the content of a document vector
print(X_train_vec_bool.shape)
print(X_train_vec_bool[0].toarray())

# check the size of the constructed vocabulary
print(len(unigram_bool_vectorizer2.vocabulary_))

# print out the first 10 items in the vocabulary
print(list(unigram_bool_vectorizer2.vocabulary_.items())[:10])

# check word index in vocabulary
print(unigram_bool_vectorizer2.vocabulary_.get('imaginative'))

#And dont forget the test data
x_test_train_bool = unigram_bool_vectorizer2.transform(X_test_train)

# print out #examples and #features in the test set
print(x_test_train_bool.shape)
# Your code ends here


# In[51]:


#Make the MNB model using the expanded ngram range
# initialize the MNB model
nb_bigram_clf= MultinomialNB()

# use the training data to train the MNB model
nb_bigram_clf.fit(X_train_vec,y_train)


# In[54]:


feature_ranks = sorted(zip(nb_bigram_clf.feature_log_prob_[0], unigram_count_vectorizer.get_feature_names_out()))
very_negative_features = feature_ranks[-10:]
print(very_negative_features)


# In[55]:


#Do the same thing as above but this time for the very positive catgory (most positive category)
feature_ranks = sorted(zip(nb_bigram_clf.feature_log_prob_[4], unigram_count_vectorizer.get_feature_names_out()))
#Counter intuitively the index remains at -10 because these are the observations which have the highest
# probability, so this is not related to positive or negative connotation. 
very_positive_features = feature_ranks[-10:]
print(very_positive_features)


# In[56]:


#Get accuracy and other measures of performance for the model 
y_pred = nb_bigram_clf.fit(X_train_vec, y_train).predict(X_test_vec)
cm2=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm2)


# In[60]:


nb_bigram_clf.score(X_test_vec, y_test)


# In[61]:


#Classification report
print(precision_score(y_test, y_pred, average=None))
print(recall_score(y_test, y_pred, average=None))

target_names = ['0','1','2','3','4']
print(classification_report(y_test, y_pred, target_names=target_names))


# In[62]:


#Fit SVM model using the expanded ngram 
svm_clf2= LinearSVC(dual=False)

# use the training data to train the MNB model
svm_clf2.fit(X_train_vec,y_train)


# In[63]:


#print accuracy
svm_clf2.score(X_test_vec,y_test)


# In[65]:


#Print confusion matrix
y_pred = svm_clf2.fit(X_train_vec, y_train).predict(X_test_vec)
cm3=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm3)


# In[66]:


#Print out report for precision and F1 score for SVM model
print(precision_score(y_test, y_pred, average=None))
print(recall_score(y_test, y_pred, average=None))

target_names = ['0','1','2','3','4']
print(classification_report(y_test, y_pred, target_names=target_names))


# In[69]:


#Setup new svm model to use 10-fold cv
unigram_bool_vectorizer_fin = CountVectorizer(encoding='latin-1', binary=True, min_df=5, ngram_range=(1,2), stop_words='english')

#import data fresh but this time wont apply the split
train2=p.read_csv("C:/Users/super/OneDrive/Desktop/train.tsv", delimiter='\t')
y=train2['Sentiment'].values
X=train2['Phrase'].values

#Apply vectorizer to whole dataset
x_vec_100 = unigram_bool_vectorizer_fin.fit_transform(X)

#Make another SVM model 
svm_fin = LinearSVC(dual=False)

#get 10 fold cross validation score to check performance of whole dataset
from sklearn.model_selection import cross_val_score
cv_score=cross_val_score(svm_fin, x_vec_100, y, cv=10, scoring="accuracy")

# Print results
print(f"Cross-validation accuracy scores: {cv_score}")
print(f"Mean accuracy: {np.mean(cv_score):.4f}")
print(f"Standard deviation: {np.std(cv_score):.4f}")


# In[71]:


from sklearn.model_selection import GridSearchCV

# Define hyperparameters to tune
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[72]:


# Define hyperparameters to tune
param_grid = {
    'C': [0.050, 0.075, 0.1, 0.25, 0.35, 0.55, 0.75]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[73]:


# Define hyperparameters to tune
param_grid = {
    'C': [0.015, 0.025, 0.035, 0.045, 0.065, 0.075, 0.085]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[74]:


# Define hyperparameters to tune
param_grid = {
    'C': [0.027, 0.029, 0.031, 0.033, 0.035, 0.037, 0.039, 0.41, 0.043]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[75]:


# Define hyperparameters to tune
param_grid = {
    'C': [100,1000]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[76]:


param_grid = {
    'tol': [0.0001, 0.00001, 0.001, 0.01, 0.1, 0.000001]  # Regularization strength
}

# Grid search with cross-validation
grid_search = GridSearchCV(LinearSVC(dual=False), param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_vec_100, y)

# Best model & accuracy
print(f"Best hyperparameter (C): {grid_search.best_params_}")
print(f"Best accuracy: {grid_search.best_score_:.4f}")


# In[88]:


#Make model with tuned hyper parameters
#Fit SVM model using the expanded 
svm_clf_tuned= LinearSVC(dual=False, C=0.039, tol=0.1, class_weight='balanced')

# use the training data to train the MNB model
svm_clf_tuned.fit(x_vec_100,y)


# In[90]:


svm_clf_tuned.score(x_vec_100, y)


# In[79]:


#Print confusion matrix
y_pred = svm_clf_tuned.fit(X_train_vec, y_train).predict(X_test_vec)
cm_tuned=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm_tuned)


# In[92]:


#Make model with tuned hyper parameters
#Fit SVM model using the expanded 
svm_clf_tuned2= LinearSVC(dual=False, C=0.039, tol=0.1)

# use the training data to train the MNB model
svm_clf_tuned2.fit(x_vec_100,y)


# In[93]:


svm_clf_tuned2.score(x_vec_100,y)


# In[94]:


y_pred = svm_clf_tuned2.fit(X_train_vec, y_train).predict(X_test_vec)
cm_tuned2=confusion_matrix(y_test, y_pred, labels=[0,1,2,3,4])
print(cm_tuned2)


# In[95]:


#Make another SVM model 
svm_fin = LinearSVC(dual=False, C=0.039, tol=0.1)

#get 10 fold cross validation score to check performance of whole dataset
from sklearn.model_selection import cross_val_score
cv_score=cross_val_score(svm_fin, x_vec_100, y, cv=10, scoring="accuracy")

# Print results
print(f"Cross-validation accuracy scores: {cv_score}")
print(f"Mean accuracy: {np.mean(cv_score):.4f}")
print(f"Standard deviation: {np.std(cv_score):.4f}")


# In[ ]:




