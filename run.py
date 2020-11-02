from preprocessor import PreProcessor
from nltk.tokenize import sent_tokenize

filePath = "C:/Users/zerad/Desktop/sujan/git_repo/preprocessor/news.docx"

prepObj = PreProcessor(
       file_path=filePath,
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

print(preprocessed)