from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import f1_score,accuracy_score
import pandas as pd
wml = WordNetLemmatizer()


def cleanToken(tokenList,additionalWords=False):
    """"
    Parameters:
        tokenList: List of tokenized words.
        additionalWords: Set to False or pass a list of additional words to remove
        from tokenList.
    Returns:
        Clean list of words.
        
    Removes English stopwords, punctionation, and additional words assigned to additionalWords.
    """
    stopwordsList = stopwords.words('english') + list(string.punctuation)
    
    if additionalWords is not False:
        stopwordsList.extend(additionalWords)
    
    cleanList = []
    for tweet in tokenList:
        clean = []
        for word in tweet:
            word = word.lower()
            if (word not in stopwordsList) and (str.isalpha(word)):
                clean.append(word)
                        
        cleanList.append(clean)
        
    return cleanList

def lemmatize_tweets(tweets):
    """
    Arguements:
    tweets- A list of clean tweets
    Returns:
    A List of lemmatize tweets
    """
    
    lemmatize_list = []
    for tweet in tweets:
        lemmatize_tweet = []
        
        for word in tweet:
            lemmatize_word = wml.lemmatize(word)
            lemmatize_tweet.append(lemmatize_word)
            
        string_tweet = " ".join(lemmatize_tweet)
        lemmatize_list.append(string_tweet)
        
    return lemmatize_list

def ModelCompare(algos,X_train,y_train,X_test,y_test):
    """
    Parameters:
        algos: Dictionary of all algorithms from sklearn to fit
        X_train: X training data
        y_train: y training data
        X_test: X testing data
        y_test: y testing data
    returns:
        data frame with training and testing accuracy scores and f1 scores
    """
    algo = []
    trainAccuracy = []
    testAccuracy = []
    f1Test = []

    for i in algos.keys():
        algo.append(i)
        model = algos.get(i)
        model.fit(X_train,y_train)

        train = model.predict(X_train)
        test = model.predict(X_test)

        trainAccuracy.append(accuracy_score(y_train,train))
        testAccuracy.append(accuracy_score(y_test,test))

        f1Test.append(f1_score(y_test,test))
        
    return pd.DataFrame({'Models':algo,'Training Accuracy':trainAccuracy,'Test Accuracy':testAccuracy,'F1 Test':f1Test})