# PREPROCESSOR

PREPROCESSOR is dedicated to provide fast development platform for developers by reducing the time consumption for textual processing.

# Requirements

 * Python 3.4 or higher

# Installation

 ```
 $ git clone https://github.com/tatkaal/preprocessor.git
 $ cd preprocessor
 $ python setup.py install
 $ pip install -r requirements.txt

 1) requires jdk version-8
	- pycontractions will only work for java version-8

   - link to download jdk:
         -- https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
   
   - link to download jre:
         -- https://www.oracle.com/java/technologies/javase-jre8-downloads.html

 2) Download pre-trained models for embeddings and contractions
	- python -m gensim.downloader --download glove-twitter-25
   - To download googlenews model
      -- https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
 ```

# Functionalities
1. Some of the features are:

   • set to lowercase
   
   • removing URLs
   
   • removing Tags and email addresses
   
   • removing Numbers/special characters
   
   • removing punctuation
   
   • removing composition
   
   • Normalization

# Usage

## Using core component
```
>>> from preprocessor import PreProcessor
>>> prepObj = PreProcessor()
```
 ### Parameters
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
 ## Using inbuilt objects
 ```
 from path_processors import local_processor, url_file_processor, url_folder_processor
 from configurations import filePath, doc_link, folder_link

 lo_output = local_processor(filePath)
 url_file_output = url_file_processor(doc_link)
 url_folder_output = url_folder_processor(folder_link)

 ```

 ## Using with Pandas Library
 ```
 Original default
 >>> dataFrame['text'] = dataFrame['text].apply(prepObj.process)
 For tweets
 >>> dataFrame['text'] = prepObj.processTweet(dataFrame['text])

 ```
 ## Using with plain text
 ```
 >>> print(prepObj.process("Pass a text here"))
 ```
 ## Add more stopwords
 ```
 >>> prepObj = PreProcessor()
 >>> prepObj.add_stopword(['this', 'and this'])
 ```