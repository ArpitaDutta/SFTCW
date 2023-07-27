import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv


cwd =os.getcwd()
bug_id=cwd.split("/")[-1]
program_name=cwd.split("/")[-6]
print(cwd)
p=0
i=-1
while i>= (-len(cwd)) :
	if cwd[i]=='/' :
		p=p+1
	if p==5 :
		break
	i=i-1
str_cwd=cwd[:i]
print(str_cwd)


start_time=datetime.now()

df_train=pd.read_csv('output.csv')

#training output dataset
y = np.array([df_train['Result']]).T
y=y.tolist()
#print y

#training input dataset
df_train.drop(['Result'],1 , inplace=True)
t_in = df_train.values.tolist()
x = np.array(t_in)
x=x.tolist()
#print len(y[0])
total_failed=np.count_nonzero(y)
total_passed=len(y)-total_failed


#print len(y)
#print len(x[0])
#print total_passed,total_failed

l1=open("Lang-1.buggy.lines")

lst=[]

for line1 in l1 :
	last_index=line1.rindex('#')
	line1=line1[:last_index]
	line1=line1.replace(".java","")
	line1=line1.replace('/','.')
	#print line1
	j=1
	l2=open("spectra")
	for line2 in l2 :
		line2=line2[:len(line2)-1]
		if line2.find("$")!= -1 :
			a=line2.index('$')
			b=line2.index('#')
			line2=line2[:a]+line2[b:]
		if line1==line2 :
			lst.append(int(j-1))
			break
		j=j+1

print lst	

b=[]
w=[]

I=math.log(float(total_failed+total_passed)/float(total_failed)+1) # I=log((h+k)/k+1) h=total_passed k=total_failed 

suspicious=[]
#print len(y)
#print len(x[0])
#print total_passed,total_failed
Ec=[0 for z in range(len(y))]
En=[0 for z in range(len(y))]
for i in range(0,len(y)):
	br=0
	for j in range(0,len(x[0])):
		if x[i][j]==1 : br=br+1    # summation of br
	Ec[i]=float(len(x[0]))/float(br)  # Ec(s)=m/summation(br)
	En[i]=float(len(x[0]))/float((len(x[0])-br+0.01)) # En(s)=m/(m-sum(br)+0.01)

nsuccess=[0 for z in range(len(x[0]))] # array to store the values of no. of success for a particular statement
nfailure=[0 for z in range(len(x[0]))] # array to store the values of no. of failure for a particular statement

for i in range(0,len(x[0])):
	for j in range(0,len(y)):
		#print x[j][i],y[j][0]
		if x[j][i]==1 and y[j][0]==0:
			nsuccess[i]=nsuccess[i]+1
		elif x[j][i]==1 and y[j][0]==1:
			nfailure[i]=nfailure[i]+1

V=[0 for z in range(len(y))]
for i in range(0,len(y)):
	Ik=0
	for j in range(0,len(x[0])):
		if x[i][j]==1 :  # if ekm=1 or this statement is covered by the test case
			Ik=nfailure[j]  # if ekm=1 then Ikm=aef where aef=nfailure for that statement
		else : Ik=0
		V[i]=V[i]+Ik  # value of v for each test case is stored here

def Sim(m,n,V,x,nfailure):  # function to calculate Sim(ti,tj)
	p=0
	Ik=0
	for i in range(0, len(x[0])):
		if x[m][i]==1 and x[n][i]==1: # if both m and n test case cover this statement then calculate the v function
			Ik=nfailure[i]
		else : Ik=0
		p=p+Ik
	return (float(p)/math.sqrt(V[m]*V[n]))
	 	
for i in range(0,len(x[0])):
	
	RC=I*math.log(float(nfailure[i])/float(total_failed-nfailure[i]+0.1)+1)
	RN=I*math.log(float(total_failed-nfailure[i])/float(total_failed-(total_failed-nfailure[i])+0.1)+1)
	Nef=0
	Nnf=0
	for k in range(0,len(y)):
		Nef=Nef+Ec[k]*RC
		Nnf=Nnf+En[k]*RN
	Nep=0
	Nnp=0
	for k in range(0,len(y)):
		W=0
		for l in range(0,len(y)):
			if x[l][i]==1 and y[l][0]==1:
				W=W+float(1-Sim(k,l,V,x,nfailure))/float(total_failed)  # W(t)=summation(1-Sim(p,ti))/Tf   here ti belongs to failed test cases
		if x[k][i]==1 : Nep=Nep+W  # Nep=summation(W(t)) where t covers this particular statement				
		else : Nnp=Nnp+W	# Nnp=summation(W(t)) where t does not cover this particular statement			
	if (Nef+Nep)!=0 and (Nnf+Nnp)!=0:
		pfe=float(Nef)/float(Nef+Nep)
		pef=float(Nef)/float(Nef+Nnf)
		pep=float(Nep)/float(Nep+Nnp)
		ppn=float(Nnp)/float(Nnf+Nnp)
		if pfe==0 or ppn==0 :
			sus_score=-999999
			suspicious.append(sus_score)
			print(str(i)+"   "+str(sus_score))
		elif pfe!=0 and ppn!=0 :
			sus_score=pef+float(ppn-pep)/float(len(y))
			suspicious.append(sus_score)
			print(str(i)+"   "+str(sus_score))
	else :
		sus_score=-999999
		suspicious.append(sus_score)
		print(str(i)+"   "+str(sus_score))
	

d = {}
for i in range(0,len(suspicious)):
	key = float(suspicious[i])
	#print key
	if key !=0:
		if key not in d:
			d[key] = []
		d[key].append(i)

for f_l in lst :
	print("**************")
	print(f_l)
	print("**************")

	ct1=0
	ct2=0
	ct3=0
	fct=0
	print("Faulty line:"+str(f_l))
	for x in sorted(d):
		print (x,len(d[x]))
		if f_l not in d[x] and fct==0:
			ct1=ct1+len(d[x])
		elif f_l not in d[x] and fct==1:
			ct3=ct3+len(d[x])
		else: 
			fct=1
			ct2=len(d[x])
	print("We have to search "+str(ct3+1)+" to "+str(ct3+ct2))
	b.append(int(ct3+1))
	w.append(int(ct3+ct2))


b_best=min(b)
best_index=b.index(int(b_best))
b_worst=w[best_index]
w_best=max(b)
worst_index=b.index(int(w_best))
w_worst=w[worst_index]

b_overallworst=0
w_overallworst=0
for i in range(len(b)):
	b_overallworst=b_overallworst+b[i]
	w_overallworst=w_overallworst+w[i]
b_avg=float(b_overallworst)/float(len(b))
w_avg=float(w_overallworst)/float(len(w))

end_time=datetime.now()
csvfile=open(str_cwd+"/COprob_wt.csv", "a+")
spamwriter1 = csv.writer(csvfile, delimiter=',')
stmt_complex=[]
stmt_complex.append(program_name);
stmt_complex.append(str(bug_id));
#stmt_complex.append(str(sys.argv[1]));
stmt_complex.append(b_best);
stmt_complex.append(b_worst);
stmt_complex.append(b_avg);
stmt_complex.append(w_avg);
stmt_complex.append(w_best);
stmt_complex.append(w_worst);
stmt_complex.append(b_overallworst);
stmt_complex.append(w_overallworst);
stmt_complex.append(start_time);
stmt_complex.append(end_time);
stmt_complex.append(end_time-start_time);
stmt_complex.append(total_passed);
stmt_complex.append(total_failed);
spamwriter1.writerow(stmt_complex);


