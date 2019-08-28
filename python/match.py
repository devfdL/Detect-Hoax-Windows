path_1 = '../data/text.txt'
f1=open(path_1, "r")
data1 =f1.read()
s = data1.split()

path_2 = '../data/new1.txt'
f2=open(path_2, "r")
data2 =f2.read()
f = data2.split()

ss= set(s)  
fs =set(f)

#print(ss.intersection(fs)) 
#print(ss.union(fs)) 
different = ss.union(fs) - ss.intersection(fs)
total = len(s) + len(f) 

score = len(different)/total*100
print('Score by different: ' + str(score) + ' %')
