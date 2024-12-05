import os
import requests
import zipfile
import io
import glob
import tarfile

def fetch_data(data_path, url):
    print(f'Fetching data from {url}')
    req = requests.get(url)
    if req.ok:
      zip = zipfile.ZipFile(io.BytesIO(req.content))
      zip.extractall(data_path)

def extract_tgz_file(data_path):
    print('Extracting .tgz file')
    tgz_file_path = glob.glob(data_path + '/**/*.tgz')[0]
    file = tarfile.open(tgz_file_path)
    destination_path = data_path + '/' + os.listdir(data_path)[0] + 'words'
    file.extractall(destination_path, filter='data')

data_path = './data'
url = 'https://git.io/J0fjL'
os.makedirs(data_path, exist_ok=True)

if len(os.listdir(data_path)) == 0:
  fetch_data(data_path, url)
  extract_tgz_file(data_path)
else:
  print("Skipping extract handwriting data, likely complete")
