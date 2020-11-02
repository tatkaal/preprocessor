# Install this
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os
import re
import io
import unidecode
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from pycontractions import Contractions
from autocorrect import Speller
from file_reader import prepare_text
from preprocessor.contractions import to_replace
from gensim import downloader as api
from configurations import pretrained_model, file_storage, token_file, credentials_json

java_path = "C:/Program Files/Java/jdk1.8.0_261/bin/java.exe"
os.environ['JAVAHOME'] = java_path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class PreProcessor():
    def __init__(self, file_path=None,doc_link=None,folder_link=None,remove_stopwords=True, lower=True, tokenize_word=True,contraction_method='mapping',
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
            # type(tokenize_sent) != bool or
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
        if file_path == None and doc_link==None and folder_link==None:
            raise Exception("Error - expecting the file path")
        self.doc = None
        self.sents = None
        self.tweets = None
        self.lemmatizer = None
        self.file_path = file_path
        self.doc_link = doc_link
        self.folder_link = folder_link
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
        # self.tokenize_sent = tokenize_sent
        self.auto_correct = auto_correct
        if self.lemmatize_method == 'wordnet':
            self.lemmatizer = WordNetLemmatizer()
        if self.lemmatize_method == 'snowball':
            self.lemmatizer = SnowballStemmer('english')
    
    def file_reader(self):
        file_content = prepare_text(self.file_path, dolower=False)
        return file_content

    def doc_downloader(self,document_link,document_type,document_name):
        # Extracting the ID from the given link
        pattern = r"(?<=d/)(.+)(?=/)"   
        DOCUMENT_ID = re.findall(pattern,document_link)[0]
        print (f"DOCUMENT ID: {DOCUMENT_ID}") 

        # Specifying the format in which the document will be downloaded
        if document_type.lower() in ['docx',"doc"]:
            file_format = "docx"
        elif document_type.lower() in ['pdf']:
            file_format = "pdf"
        else:
            print ("Document Format Not Supported. Only Docs, Doc and PDF are supported")
            return None

        creds = None
        
        if os.path.exists(token_file):
            with open(token_file,'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_json,SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file,'wb') as token:
                pickle.dump(creds,token)
        service = build('drive','v3',credentials=creds)

        file_name = '.'.join([document_name,file_format])
        try:
            print ("Downloading file")
            request = service.files().get_media(fileId=DOCUMENT_ID)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh,request=request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print (f"Download {status.progress()*100}")
        except:
            print ("Downloading MS Word Document file")
            request = service.files().export_media(fileId=DOCUMENT_ID,mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh,request=request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print (f"Download {status.progress()*100}")
                
        fh.seek(0)
        with open(os.path.join(file_storage,file_name),'wb') as f:
            f.write(fh.read())
            f.close()
            print("SAVED")

    def folder_downloader(self,folder_link):
        # Extracting the ID from the given link
        pattern = r'(?<=folders/)(\w+)'   
        DOCUMENT_ID = re.findall(pattern,folder_link)[0]
        print (f"DOCUMENT ID: {DOCUMENT_ID}")

        creds = None
        
        if os.path.exists(token_file):
            with open(token_file,'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_json,SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file,'wb') as token:
                pickle.dump(creds,token)
        service = build('drive','v3',credentials=creds)

        listofFiles = []
        page_token = None
        # docx_query = f"'{DOCUMENT_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'"
        # pdf_query = f"'{DOCUMENT_ID}' in parents and mimeType='application/pdf'"
        # txt_query = f"'{DOCUMENT_ID}' in parents and mimeType='text/plain'"
        query = f"'{DOCUMENT_ID}' in parents"
        while True:
            response = service.files().list(
                q=query,
                fields='nextPageToken, files(id, name)',
                pageToken = page_token,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()
            for file in response.get('files',[]):
                listofFiles.append(file)

            page_token = response.get('nextPageToken',None)
            if page_token is None:
                break

        for item in listofFiles:
            document_id = item['id']
            file_name = item['name']
            name_splitted = file_name.split(".")
            if len(name_splitted) == 1:
                file_name = '.'.join([file_name,"docx"])
            try:
                print ("Downloading docx file")
                print (file_name)
                request = service.files().get_media(fileId=document_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fd=fh,request=request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print (f"Download {status.progress()*100}")
            except:
                print ("Downloading doc file")
                print (file_name)
                request = service.files().export_media(fileId=document_id,mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fd=fh,request=request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print (f"Download {status.progress()*100}")
            fh.seek(0)
            with open(file_storage+'/'+file_name,'wb') as f:
                f.write(fh.read())
                f.close()

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
        # if(self.tokenize_sent==False):
        #     self.doc = sent_tokenize(self.doc)
        if(self.tokenize_word==False):
            self.tokenize_word_fun()
        if self.embedding_method == 'glove':
            model = api.load("glove-twitter-25")
            vecs=[]
            for x in self.doc:
                vec = [model[i] for i in x]
                vecs.append(vec)
                self.doc = vecs
            # print(vecs)
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
            model = pretrained_model
            cont = Contractions(model)
            cont.load_models()
            self.doc = list(cont.expand_texts([str(self.doc)],precise=True))[0]
        elif self.contraction_method == 'glove':
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
        """tokenizes the sentences to words"""
        self.doc = word_tokenize(self.doc)
    
    # def tokenize_sent_fun(self):
    #     """tokenizes the paragraphs to sentences"""
    #     self.sents = sent_tokenize(self.doc)

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
        elif self.lemmatize_method == 'snowball':
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

    def process(self):
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
        if self.file_path != None:
            data = self.file_reader()
        if self.doc_link != None:
            self.doc_downloader(self.doc_link,"docx","testing_document")
            path = file_storage+'/testing_document.docx'
            data = prepare_text(path, dolower=False)
        if self.folder_link != None:
            self.folder_downloader(self.folder_link)
            data = 'test'
        output=[]
        self.sents = sent_tokenize(data)
        for doc in self.sents:
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
            output.append(self.doc)
        return output

def local_processor(path):
      prepObj = PreProcessor(
            file_path=path,
            lower=True,
            tokenize_word=False, #if false the output will be in list of sentences
            remove_stopwords=True,
            remove_numbers=True,
            remove_html_tags=True,
            remove_punctuations=True,
            remove_accented_chars=True,
            remove_whitespace=True,
            auto_correct=True,
            lemmatize_method='snowball',
            embedding_method='word2vec',
            contraction_method='mapping',
            )
      preprocessed = prepObj.process()
      with open(file_storage+'/local_processed.txt','w', encoding='utf-8') as f:
            f.write(str(preprocessed))
      return preprocessed

def url_file_processor(path):
      prepObj = PreProcessor(
            doc_link=path,
            lower=True,
            tokenize_word=False, #if false the output will be in list of sentences
            remove_stopwords=True,
            remove_numbers=True,
            remove_html_tags=True,
            remove_punctuations=True,
            remove_accented_chars=True,
            remove_whitespace=True,
            auto_correct=True,
            lemmatize_method='snowball',
            embedding_method='word2vec',
            contraction_method='mapping',
            )
      preprocessed = prepObj.process()
      with open(file_storage+'/url_file_processed.txt','w', encoding='utf-8') as f:
            f.write(str(preprocessed))
      return preprocessed

def url_folder_processor(path):
      prepObj = PreProcessor(
      folder_link=path,
      lower=True,
      tokenize_word=False, #if false the output will be in list of sentences
      remove_stopwords=True,
      remove_numbers=True,
      remove_html_tags=True,
      remove_punctuations=True,
      remove_accented_chars=True,
      remove_whitespace=True,
      auto_correct=True,
      lemmatize_method='snowball',
      embedding_method='word2vec',
      contraction_method='mapping',
      )
      preprocessed = prepObj.process()
      with open(file_storage+'/url_folder_processed.txt','w', encoding='utf-8') as f:
            f.write(str(preprocessed))
      return preprocessed