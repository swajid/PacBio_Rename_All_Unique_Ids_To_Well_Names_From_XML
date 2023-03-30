#!/usr/bin/env python
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
import fnmatch

pacbio_directory = r'\\***\BioInfoProjects\***'
path = pacbio_directory
files = os.listdir(path)
paths = []

#Find all *consensusreadset.xml in all subdirectories
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".xml"):
            if fnmatch.fnmatch(file, '*consensusreadset.xml'):
                 print(os.path.join(root, file))
                 s = os.path.join(root, file)
                 paths.append(s)

#initialize data frame
df = pd.DataFrame(columns=('Shipping_Id','Movie_Id', 'WellName', 'FileName', 'Unique_Id'))

#pull data via tags from each xml file
for k in paths:
    print(k)
    with open(k, 'r') as f:
        file = f.read() 
    soup = BeautifulSoup(file, 'xml')
    well_name = soup.find('WellName')
    file_name = soup.find("pbbase:ExternalResources").find("pbbase:FileIndices").find("pbbase:FileIndex").get("ResourceId")
    movie_id = file_name.split(".")[0]
    shipping_id = soup.find("pbds:DataSetMetadata").find("pbmeta:Collections").find("pbmeta:WellSample").get("Name")
    unique_id = soup.find("pbds:ConsensusReadSet").get("UniqueId")
    df = df.append({'Shipping_Id':shipping_id, 'Movie_Id':movie_id, 'WellName':well_name.string, 'FileName':file_name, 'Unique_Id':unique_id}, ignore_index=True)

# save df to excel if you'd like
#df.to_excel("***_Shipping_Ids_Files.xlsx", index=0)
    
# output shell script commands to rename folders
print("#!/bin/bash")
for index, row in df.iterrows():
    folder_name = row['Unique_Id']
    well_name = row['WellName']
    regex = "'s/"+folder_name+"/"+well_name+"/g'"
    print("find . -type d -name '"+folder_name+"' | while read f; do mv $f $(echo $f | sed "+regex+"); done")
 


