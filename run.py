# from path_processors import local_processor, url_file_processor, url_folder_processor

from preprocessor.preprocessor import local_processor, url_file_processor, url_folder_processor
from configurations import filePath, doc_link, folder_link

lo_output = local_processor(filePath)
# print(lo_output)

url_file_output = url_file_processor(doc_link)
print(url_file_output)

url_folder_output = url_folder_processor(folder_link)
# print(url_folder_output)