"""
    pip install pandas
    
    Fix warning: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.
    pyenv uninstall 3.8.0
    sudo apt-get install liblzma-dev
    pyenv install 3.8.0
"""

import pandas as pd

# names of files to read from
r_filenameCSV = 'csv_tsv_files/branlytic.csv'
r_filenameTSV = 'csv_tsv_files/Spotify_SpotifyDuo_NO_NOK_20200101-20200131.tsv.gz'

# names of files to write to
w_filenameCSV = 'csv_tsv_files/branlytic.output.csv'
w_filenameTSV = 'csv_tsv_files/Spotify_SpotifyDuo_NO_NOK_20200101-20200131.output.tsv.gz'

# read the data
csv_read = pd.read_csv(r_filenameCSV)
tsv_read = pd.read_csv(r_filenameTSV, sep='\t')

# print the first 10 records
print(csv_read.head(10))
print(tsv_read.head(10))

# write to files
with open(w_filenameCSV,'w') as write_csv:
    write_csv.write(tsv_read.to_csv(sep=',', index=False))

with open(w_filenameTSV,'w') as write_tsv:
    write_tsv.write(csv_read.to_csv(sep='\t', index=False))