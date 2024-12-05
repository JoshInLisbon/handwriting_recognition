import os
import requests
import zipfile
import io
import glob
import tarfile

def fetch_data(data_path, url):
  if len(os.listdir(data_path)) == 0:
    print(f'Fetching data from {url}')
    req = requests.get(url)
    if req.ok:
      zip = zipfile.ZipFile(io.BytesIO(req.content))
      zip.extractall(data_path)
  else:
    print('Skipped fetching data')

def extract_tgz_file(data_path, png_path):
  destination_path = data_path + png_path
  if len(os.listdir(destination_path)) == 0:
    print('Extracting .tgz file')
    tgz_file_path = glob.glob(data_path + '/**/*.tgz')[0]
    file = tarfile.open(tgz_file_path)
    file.extractall(destination_path, filter='data')
  else:
    print('Skipping .tgz extraction')

data_path = './data'
url = 'https://git.io/J0fjL'
png_path = '/word_pngs'
os.mkdir(data_path + png_path)

fetch_data(data_path, url)
extract_tgz_file(data_path, png_path)
