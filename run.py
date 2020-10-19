from preprocessor import PreProcessor
from nltk.tokenize import sent_tokenize

prepObj = PreProcessor(
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
contents = prepObj.file_reader("C:/Users/zerad/Desktop/sujan/git_repo/preprocessor/news.docx")
example = sent_tokenize(contents)
preprocessed = [prepObj.process(i) for i in example]
print(preprocessed)