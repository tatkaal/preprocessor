from preprocessor import PreProcessor

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

print(prepObj.process("wrld Pass               café   12,13  'is isn't ain't text here @ for getting nice @here +23 google https://github.com/tatkaal/preprocessor"))
