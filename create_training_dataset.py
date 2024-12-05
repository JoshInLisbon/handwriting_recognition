import glob
import os
import csv
import extract_handwriting_data

data_path = extract_handwriting_data.data_path
text_file = glob.glob(data_path + '/**/*.txt')[0]
pngs_path = glob.glob(data_path + '/*/*/')[0]

def text_file_to_data(text_file):
  for line in open(text_file, 'r').readlines():
    # avoid comments
    if line.startswith('#'):
      continue

    split_line = line.split(' ')
    # avoid data with errors
    if split_line[1] == 'err':
        continue

    yield split_line

def path_from_id(id):
  spl = id.split('-')
  return f'{spl[0]}/{spl[0]}-{spl[1]}/{id}.png'

def create_dataset(destination, text_file, pngs_path):
  characters, max_label_len = set(), 0
  os.makedirs(destination, exist_ok=True)

  with open(destination + 'training_data.csv', 'w') as training_csv:
    writer = csv.writer(training_csv)
    writer.writerow(['png_path', 'label'])

    for data in text_file_to_data(text_file):
      png_path = pngs_path + path_from_id(data[0])
      # ensure png exists
      if not os.path.exists(png_path):
        continue

      label = data[-1].rstrip('\n')
      writer.writerow([png_path, label])
      characters.update(list(label))
      max_label_len = max(max_label_len, len(label))

  with open(destination + 'metadata.csv', 'w') as meta_csv:
    writer = csv.writer(meta_csv)
    writer.writerow(['characters'] + list(characters))
    writer.writerow(['max_label_len', max_label_len])

destination = './processed_data/'
create_dataset(destination, text_file, pngs_path)