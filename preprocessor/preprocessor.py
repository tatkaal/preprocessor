to_replace = {"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "iit will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that had",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there had",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they had",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"}



import re
import unidecode
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from pycontractions import Contractions
from autocorrect import Speller

import os
java_path = "C:/Program Files/Java/jdk1.8.0_261/bin/java.exe"
os.environ['JAVAHOME'] = java_path

class PreProcessor():
    def __init__(self, remove_stopwords=True, lower=True, tokenize_word=True, contraction_method='mapping',
                 remove_numbers=True, remove_html_tags=True,
                 remove_punctuations=True, remove_accented_chars=True, remove_whitespace=True,
                 lemmatize_method='wordnet',
                 embedding_method='word2vec',
                 auto_correct=True):
        """
        This package contains functions that can help during the
        preprocessing of text data.
        :param remove_stopwords: boolean
            default value = True
        :param replace_words: str
            default value = regex
        """
        if (type(remove_stopwords) != bool or
            type(lower) != bool or
            type(tokenize_word) != bool or
            type(remove_numbers) != bool or
            type(remove_html_tags) != bool or
            type(remove_punctuations) != bool or
            type(remove_accented_chars) != bool or
            type(auto_correct) != bool or
            type(remove_whitespace) != bool):
            raise Exception("Error - expecting a boolean parameter")
        if lemmatize_method not in ['wordnet', 'snowball']:
            raise Exception("Error - lemmatizer method not supported")
        else:
            self.lemmatize = True
        if contraction_method not in ['glove','word2vec','mapping']:
            raise Exception("Error - contraction method not supported")
        else:
            self.contractions = True
        if embedding_method not in ['glove','word2vec','bow']:
            raise Exception("Error - embedding method not supported")
        else:
            self.word_embedding = True
        self.doc = None
        self.tweets = None
        self.lemmatizer = None
        self.lower = lower
        self.remove_stopwords = remove_stopwords
        self.contraction_method = contraction_method
        self.embedding_method = embedding_method
        self.remove_numbers = remove_numbers
        self.remove_html_tags = remove_html_tags
        self.remove_punctations = remove_punctuations
        self.remove_accented_chars = remove_accented_chars
        self.remove_whitespace = remove_whitespace
        self.lemmatize_method = lemmatize_method
        self.stopword_list = stopwords.words('english')
        self.replacement_list = to_replace
        self.tokenize_word = tokenize_word
        self.auto_correct = auto_correct
        if self.lemmatize_method == 'wordnet':
            self.lemmatizer = WordNetLemmatizer()
        if self.lemmatize_method == 'snowball':
            self.lemmatizer = SnowballStemmer('english')
    
    def lower_fun(self):
        """
        This function converts text to lower
        """
        self.doc = self.doc.lower()

    def remove_stopwords_fun(self):
        """
        This function removes stopwords from doc.
        It works by tokenizing the doc and then
        checking if the word is present in stopwords
        """
        # tokens = str(self.doc).split()
        tokens = word_tokenize(self.doc)
        cleaned_tokens = [token for token in tokens if token.lower() not in self.stopword_list]

        self.doc = ' '.join(cleaned_tokens)

    def word_embedding_fun(self):
        if self.embedding_method == 'glove':
            pass            
        elif self.embedding_method == 'word2vec':
            pass
        elif self.embedding_method == 'bow':
            pass

    def mapping_decontraction(self,phrase):
        cleaned_doc = []
        for word in str(self.doc).split():
            if word.lower() in self.replacement_list.keys():
                cleaned_doc.append(self.replacement_list[word.lower()])
            else:
                cleaned_doc.append(word)
        phrase = ' '.join(cleaned_doc)
        return phrase

    def contractions_fun(self):
        """
        This function replaces words that are --
        by checking a word if a word is present in a dictionary
        if the word is present in dictionary then it is replaced
        with its value from dictionary
        """
        if self.contraction_method == 'mapping':
            self.doc = self.mapping_decontraction(str(self.doc))
        elif self.contraction_method == 'word2vec':
            model = "GoogleNews-vectors-negative300.bin"
            cont = Contractions(model)
            cont.load_models()
            self.doc = list(cont.expand_texts([str(self.doc)],precise=True))[0]
        elif self.contraction_method == 'glove':
            import gensim.downloader as api
            model = api.load("glove-twitter-25")
            cont = Contractions(kv_model=model)
            cont.load_models()
            self.doc = list(cont.expand_texts([str(self.doc)],precise=True))[0]

    def remove_numbers_fun(self):
        """
        This function uses regex to remve
        all the numbers from the doc.
        """
        self.doc = re.sub("[0-9]", "", self.doc)
        self.doc = self.doc.strip()
        self.doc = " ".join(self.doc.split())
    
    def autocorrect_fun(self):
        spell = Speller(lang='en')
        self.doc = [spell(w) for w in word_tokenize(self.doc)]

    def remove_html_tags_fun(self):
        """
        This function uses regex's complile method
        to remove all the HTML tags from the doc
        """
        cleaner = re.compile('<.*?>')
        cleaned_text = re.sub(cleaner, '', self.doc)
        cleaned_text = re.sub('[\n\t]', '', cleaned_text)
        self.doc = cleaned_text.strip()
        self.doc = " ".join(self.doc.split())

    def remove_punctations_fun(self):
        """
        This function uses regex to remove alk the
        punctations from the doc.
        """ 
        self.doc = re.sub('[^a-zA-Z0-9]', ' ', self.doc)
        self.doc = self.doc.strip()
        self.doc = " ".join(self.doc.split())

    def remove_accented_chars_fun(self):
        """remove accented characters from text, e.g. café"""
        self.doc = unidecode.unidecode(self.doc)
    
    def remove_whitespace_fun(self):
        """remove extra whitespaces from text"""
        text = self.doc.strip()
        self.doc = " ".join(text.split())

    def tokenize_word_fun(self):
        """tokenizes the sentences"""
        self.doc = word_tokenize(self.doc)

    def lemmatize_fun(self):
        """
        This function applies the stemming to the words
        It can be operated with either WordNetLemmatizer
        or Snowball Stemmer
        ---------------------------
        Example:
        lemmatize(method='snowball')
        
        default value = 'wordnet
        """
        cleaned_tokens = None
        if self.lemmatize_method == 'wordnet':
            cleaned_tokens = [self.lemmatizer.lemmatize(token) for token in self.doc]
        else:
            cleaned_tokens = [self.lemmatizer.stem(token) for token in self.doc]
       
        self.doc = ' '.join(cleaned_tokens)

    def add_stopword(self, *args):
        """
        This function is used to add new stopwords
        to the predefined list
        Parameters - ["new_stopword"]
        ------------------------------
        Example -
        obj = NLP()
        obj.add_stopword(["first_word", "second_word"])
        """
        if self.remove_stopwords is False:
            raise Exception("Please enable removal of stopwords")
        if type(args) != list:
            raise Exception("Error - pass stopwords in list")
        for arg in args:
            self.stopword_list.add(arg)

    def print_stopwords(self):
        """
        This function prints all the stopwords
        that are present in the list
        Return Type - list
        ------------------------------
        Example
        obj = NLP()
        obj.print_stopwords()
        """
        if self.stopword_list == []:
            raise Exception("Error - stopword list is empty")
        print(self.stopword_list)

    def process(self, doc):
        """
        This function processes the doc
        If the remove_stopwords flag is True
            - it will remove stopwords from doc
        If the clean_words flag is True
            - it will clean the doc by replacing words
        Parameters - [doc]
        ------------------------------
        Example
        obj = NLP()
        obj.process(["process this text"])

        How to use with pandas?
        obj = NLP()
        df = df['text].apply(obj.process)
        """
        self.doc = doc
        if self.lower is True:
            self.lower_fun()
        if self.contractions is True:
            self.contractions_fun()
        if self.remove_html_tags is True:
            self.remove_html_tags_fun()
        if self.remove_numbers is True:
            self.remove_numbers_fun()
        if self.remove_punctations is True:
            self.remove_punctations_fun()
        if self.remove_accented_chars is True:
            self.remove_accented_chars_fun()
        if self.remove_stopwords is True:
            self.remove_stopwords_fun()
        if self.remove_whitespace is True:
            self.remove_whitespace_fun()
        if self.auto_correct is True:
            self.autocorrect_fun()
        if self.lemmatize is True:
            self.lemmatize_fun()
        if self.tokenize_word is True:
            self.tokenize_word_fun()
        if self.word_embedding is True:
            self.word_embedding_fun()
        return self.doc