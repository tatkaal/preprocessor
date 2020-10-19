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
        replace_words=True,
        remove_stopwords=True,
        remove_numbers=True,
        remove_HTML_tags=True,
        remove_punctation=True,
        lemmatize=False,
        lemmatize_method='wordnet'
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
 ## Add more replace words
 ```
 >>> prepObj = PreProcessor()
 >>> prepObj.add_replacement([this="by this", this="by this"])
 ```