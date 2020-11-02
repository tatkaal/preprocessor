import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
file_storage = os.path.join(ROOT,'temp_files')

'''<--------------------------File Paths------------------------------>'''
filePath = os.path.join(ROOT,'temp_files/news.docx')
doc_link = "https://docs.google.com/document/d/1HxKzFzJL4oymI1Jswru_mw9GCHu--YJa7cb7Xnx13dM/edit?usp=sharing"
folder_link = "https://drive.google.com/drive/folders/14UuKNktEAalwkVKQrNdZBUJV_WS80jDy?usp=sharing"

'''<-----pretrained model --->'''
pretrained_model = os.path.join(ROOT, "models/GoogleNews-vectors-negative300.bin")

'''<-----drive link downloader requirement file--->'''
token_file = os.path.join(ROOT, "models/token.pickle")
credentials_json = os.path.join(ROOT, "models/credentials.json")