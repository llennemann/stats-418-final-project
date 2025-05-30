# script to merge all data into one csv
import os
import gzip
import shutil
import pandas as pd

my_data_path = '/Users/lucy/Downloads'
dest_path = '/Users/lucy/Desktop/UCLA/pems_data'

os.chdir(dest_path)
print(os.getcwd()) # print current working directory

pems_data = [f for f in os.listdir(path=".") if 'text_station_5min_2024' in f]

# Output CSV file path
output_path = "merged.csv"

for file in pems_data:
    print("Processing:", file)
    # move file from Downloads to pems_data folder
    # print(shutil.move(my_data_path + '/' + file, dest_path + '/' + file))
    with gzip.open(file, 'rt') as f:
        curr_df = pd.read_csv(f)
        # Append to CSV file with mode=a
        curr_df.to_csv(output_path, mode='a', header=False, index=False)