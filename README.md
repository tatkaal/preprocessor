# PREPROCESSOR

PREPROCESSOR is dedicated to provide fast development platform for developers by reducing the time consumption for textual processing.

# Requirements

 * Python 3.4 or higher

# Installation


 ### From GIT
 ```
 $ git clone https://github.com/tatkaal/preprocessor.git
 $ cd preprocessor
 $ python setup.py install
 ```

# Functionalities
1. Features are:
   
   • set to lowercase
   
   • removing URLs
   
   • removing Tags and email addresses
   
   • removing Numbers/special characters
   
   • removing punctuation
   
   • removing composition
   
   • Normalization

# Usage
```
>>> from preprocessor import PreProcessor
>>> prepObj = PreProcessor()
```
 ## Parameters
 ```
 >>> prepObj = PreProcessor(
       lower=True,
       tokenize_word=True,
       contraction_method='mapping',
       remove_stopwords=True,
       remove_numbers=True,
       remove_html_tags=True,
       remove_punctuations=True,
       remove_accented_chars=True,
       remove_whitespace=True,
       auto_correct=True,
       lemmatize_method='wordnet',
      embedding_method='word2vec'
      )
 ```
 ## Using with Pandas Library
 ```
 Original default
 >>> dataFrame['text'] = dataFrame['text].apply(prepObj.process)
 For tweets
 >>> dataFrame['text'] = prepObj.processTweet(dataFrame['text])

 ```
 ## Using with plain textx
 ```
 >>> print(prepObj.process("Pass a text here"))
 ```
 ## Add more stopwords
 ```
 >>> prepObj = PreProcessor()
 >>> prepObj.add_stopword(['this', 'and this'])
 ```