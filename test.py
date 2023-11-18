import os
import shutil
import tempfile
from zipfile import ZipFile


temp_dir = tempfile.mkdtemp()


def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        # print(root)
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths

zip_filename = "archive.zip"
zip_filepath = os.path.join(temp_dir, zip_filename)

file_paths = get_all_file_paths('users')
print(file_paths)

with ZipFile(zip_filename, 'w') as zipf:
    for file in file_paths: 
        filename = file.rsplit("\\",1)[1]
        zipf.write(file,filename) 

shutil.rmtree(temp_dir)