import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv


start=datetime.now()
with open('statementResult.csv','r') as in_file, open('uniqueResult.csv','w') as out_file:
	seen = set() # set for fast O(1) amortized lookup
	for line in in_file:
		if line in seen: 
			continue 
		else: 
			seen.add(line)
			out_file.write(line)
t1= (datetime.now() - start)

cwd =os.getcwd()
version=cwd.split("/")[-1]
program_name=cwd.split("/")[-2].split("_")[0]
print(cwd)
str_cwd=cwd.replace("/"+version,"")
print(str_cwd)


df_train=pd.read_csv('statementResult.csv')
y = np.array([df_train['Result']]).T
y=y.tolist()
total_failed=np.count_nonzero(y)
total_passed=len(y)-total_failed


df_train1=pd.read_csv('uniqueResult.csv')
y1 = np.array([df_train1['Result']]).T
y1=y1.tolist()
unique_failed=np.count_nonzero(y1)
unique_passed=len(y1)-unique_failed

cwd=cwd.replace("/"+version, "")

csvfile=open(cwd+"/uniquenessResults.csv", "a+")
spamwriter1 = csv.writer(csvfile, delimiter=',')
stmt_complex=[]
stmt_complex.append(program_name);
stmt_complex.append(str(version));
stmt_complex.append(total_passed);
stmt_complex.append(total_failed);
stmt_complex.append(total_failed+total_passed);
stmt_complex.append(unique_passed);
stmt_complex.append(unique_failed);
stmt_complex.append(unique_failed+unique_passed);
stmt_complex.append(t1);
spamwriter1.writerow(stmt_complex);

	
		
	

