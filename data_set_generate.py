from random import *
import random

test_case=50
p=1
all_sample=[]
minimum_ground_set=5
maximum_ground_set=10
minimum_weight_value=1
maximum_weight_value=5

while(p<=test_case):
    sample={}
    ground_set_total=(randint(minimum_ground_set,maximum_ground_set))
    sample["ground_set_total"]=ground_set_total
    print(ground_set_total)
    ground_set=set()
    for i in range(1,ground_set_total+1,1):
        ground_set=ground_set.union([i])
    if(ground_set_total>6):
        number_of_subset=pow(2,(ground_set_total-5))-1
    else:
        number_of_subset=pow(2,(ground_set_total-2))-1
    sample["subset_total"]=number_of_subset
    #print(ground_set)

    check=set()
    set_subset=[[]for k in range(number_of_subset)]
    #print(set_subset)
    weight=[]
    for j in range(1,number_of_subset+1,1):

        while(True):
            subset_element_number=(randint(1,ground_set_total))
            subset=random.sample(ground_set, subset_element_number)
            #print(subset)
            if(subset not in set_subset):
                check=check.union(subset)
                set_subset[j-1]=subset
                weight.append(round(random.uniform(minimum_weight_value,maximum_weight_value),2))
                break;
            else:
                continue;
        
        
    if(ground_set==check):
        print("test case:: %d" %p)
        p=p+1
        print(ground_set)
        print(set_subset)
        sample["set_subset"]=set_subset
        sample["weight"]=weight
        all_sample.append(sample)

with open('testcase1_generate.txt', 'w') as f:

    f.write(str(len(all_sample))+"\n")
    for s in all_sample:
        f.write(str(s["ground_set_total"])+"\n")
        f.write(str(s["subset_total"])+"\n")
        for m in range(len(s["set_subset"])):
            f.write(str(s["weight"][m])+" "+str(len(s["set_subset"][m]))+" ")
            for n in s["set_subset"][m]:
                f.write(str(n)+" ")
            f.write("\n")
            
