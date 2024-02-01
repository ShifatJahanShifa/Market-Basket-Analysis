from itertools import combinations
import re

totalResult=[]
def readTransaction(fileName):
    outputList=[]
    with open(fileName,'r') as file:
        for line in file:
            line=line.strip()
            if line:
                #parts=line.split()
                parts=re.split(r'[,\s]+', line)
                outputList.append([parts[0],parts[1:]]) 
    return outputList
        
def frequentOneItemList(transaction):
    uniqueItem=[]
    for item1 in transaction:
        for item2 in item1[1]:
            if item2 not in uniqueItem: 
                uniqueItem.append(item2) 
    uniqueItem.sort()
    return uniqueItem

def Join(Li,itemSize):
    oldList=[item for item in Li.keys()]
    # print(oldList)
    newLists=[]
    for i in range(0,len(oldList)):
        for j in range(i+1,len(oldList)):
            temp=(oldList[i]).union((oldList[j]))
            if len(temp)==itemSize:
                if itemSize==2:
                    newLists.append((temp))
                else: 
                    if pruning(Li,temp,itemSize-1): 
                        temp.clear()
                    else:
                        newLists.append((temp)) 

    newLists.sort()
    return newLists

def pruning(Li,temp,size):
    subsets=list(combinations(temp,size))

    for set in subsets:
        if set not in Li.keys():
            return False 
    return True

def apriori(transaction,supportCount):
    #for the frequent 1-itemlist
    uniqueItem=frequentOneItemList(transaction)
    C1={}
    for item in uniqueItem:
        for data in transaction:
            if item in data[1]:
                if item in C1.keys():
                    C1[item]+=1
                else:
                    C1[item]=1 
    
    print("Candidate List for frequent 1-itemset\n")
    for item in C1.keys():
        print(str(item)+":"+str(C1[item]))
    print()
    # final frequent 1-itemset
    L1={}

    for item,count in zip(C1.keys(),C1.values()): 
        if count>=supportCount:
            if item in L1:
                L1[frozenset([item])]+=count
            else:
                L1[frozenset([item])]=count  

    print("frequent 1-itemset: \n")
    for item in L1.keys():
        print(str(item)+":"+str(L1[item]))
    print()

    totalResult.append(L1);
    Li=L1.copy()

    for itemSize in range(2,1000):
        newItems=Join(Li,itemSize)
        # newItem=set(newItems)
        #scanning database
        Ci={}
        for item in newItems:
            Ci[item]=0
            for value in transaction:
                temp=set(value[1])
                if item.issubset(temp):
                    Ci[item]+=1 
        #print("Candidate List: frequent "+str(itemSize)+"-itemset\n"+str(Ci)+"\n")
        #print(f"Candidate List: frequent {itemSize}-itemlist:\n{Ci}\n")
        print(f"Candidate List for frequent {itemSize}-itemset\n")
        for item in Ci.keys():
            print(str(item)+":"+str(Ci[item]))
        print()

        Li={}
        for item in Ci.keys():
            if Ci[item]>=supportCount:
                Li[item]=Ci[item]

        #print("frequent "+itemSize+"-itemset: \n"+str(Li)+"\n")
        #print(f"frequent {itemSize}-itemlist\n{Li}\n")
        print(f"frequent {itemSize}-itemset: \n")
        for item in Li.keys():
            print(str(item)+":"+str(Li[item]))
        print()

        if len(Li)==0: return
        else: totalResult.append(Li)



fileName='C:\\Users\\HP\\OneDrive\\Desktop\\DBMS-Code\\input1.txt'
transaction=readTransaction(fileName) 
supportCount=2
apriori(transaction,supportCount)
#print(len(totalResult))
length=len(totalResult)
for item in totalResult[len(totalResult)-1].keys():
    print(str(item)+":"+str(totalResult[length-1][item]))

    l=len(item)
    for i in range(1,l):
        subsets=list(combinations(item,i))
        print(subsets)
        for j in subsets:
            #print("here")
            jf=frozenset(j)
            #print(jf)
            if jf in totalResult[i-1].keys():
                up=totalResult[i-1][jf]
                #print("here")
                print(str(jf)+"/"+str(item)+"= "+str(totalResult[length-1][item])+"/"+str(up)+" = "+str((totalResult[length-1][item]/up)))
        print()
#now calculate confidence
    