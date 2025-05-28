# script to unzip and clean files
import os
import gzip

my_data_path = '/Users/lucy/Downloads/'

os.chdir(my_data_path)
print(os.getcwd()) # print current working directory

print(os.listdir(path=".")) 
# filter files that we want
pems_data = [f for f in os.listdir(path=".") if 'text_station' in f]

for file in pems_data:
    if file.endswith('.gz'):
        gzip.decompress(file)
