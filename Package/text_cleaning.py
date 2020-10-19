import re
import string
import unidecode

def clean(text,lowercase=False,punct=False,url=False,html=False):
    if lowercase:
        text = text.lower()
    if punct:
        if punct and url and html:
            url_pattern = re.compile(r'https?://\S+|www\.\S+')
            text = re.sub(url_pattern,'',text)
            html_pattern = re.compile('<.*?>')
            text = re.sub(html_pattern,'',text)
            punctuations = string.punctuation
            text = text.translate(str.maketrans('','',punctuations))
        elif punct and url:
            url_pattern = re.compile(r'https?://\S+|www\.\S+')
            text = re.sub(url_pattern,'',text)
            punctuations = string.punctuation
            text = text.translate(str.maketrans('','',punctuations))
        elif punct and html:
            html_pattern = re.compile('<.*?>')
            text = re.sub(html_pattern,'',text)
            punctuations = string.punctuation
            text = text.translate(str.maketrans('','',punctuations))
        else:
            punctuations = string.punctuation
            text = text.translate(str.maketrans('','',punctuations))
            text.translate
    if url:
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text = re.sub(url_pattern,'',text)
    if html:
        html_pattern = re.compile('<.*?>')
        text = re.sub(html_pattern,'',text)

    text = unidecode.unidecode(text)
    # text = re.sub(" +"," ",text)
    # text = re.sub("\n+","\n",text)
    text = re.sub("\s+"," ",text)
    text = text.strip()
    return text

print(clean("Here @ are #$ can't lots of punct.", punct=True,lowercase=True,url=True))