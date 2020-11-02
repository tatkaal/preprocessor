from preprocessor import PreProcessor
from configurations import file_storage

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