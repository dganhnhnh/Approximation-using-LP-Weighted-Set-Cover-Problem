from pulp import *
import time
import csv

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)



class Set_Cover:

    def __init__(self,prob_spec):
        #print(prob_spec)
        self.total_element=prob_spec["total_element"]
        self.weight= prob_spec["weight"]
        self.total_subset= prob_spec["total_subset"]
        self.set_subset= prob_spec["set_subset"]
        self.ground_set = set()
        self.lp_result =[]
        self.cost=0
        #self.bit_mask_memory=[{} for count in range(self.total_subset)]
        self.subset_mask=[]
        
    def lp_solver(self):
        self.lp_result=[]
        self.cost=0.0
        
        _lp_prob = LpProblem(LpMinimize)
        _lp_vars = LpVariable.dicts("DecisionVars",
                                         self.decision_vars,
                                         0,1,cat='Continuous')
        #objective function
        _lp_prob += sum([self.weight[self.decision_vars.index(x)] * _lp_vars[x] for x in self.decision_vars])

        for count in range(self.total_element):
            _lp_prob +=sum([_lp_vars[subset_no+1] for subset_no in self.frequency_list[count]])>=1

        _lp_prob.solve()

        self.decision_vars=[]
        for variable in _lp_prob.variables():
            self.decision_vars.append(variable.varValue)

        for count in range(len(self.decision_vars)):
            if self.decision_vars[count]>= 1.0/self.max_frequency:
                self.decision_vars[count]=1.0
                self.lp_result.append(count)
            else:
                self.decision_vars[count]=0.0
        
        self.cost = sum([self.weight[count]* self.decision_vars[count] for count in range(len(self.decision_vars))])

        return (self.lp_result,self.cost)

        
            
        
        
    def problem_formulate(self):
        
        for subset in self.set_subset:
            self.ground_set=self.ground_set.union(subset)
        self.ground_set = list(self.ground_set)
        #print(self.ground_set)
        self.decision_vars = [var for var in range(1,self.total_subset+1,1)]
        self.frequency_list=[[subset_no for subset_no in range (len(self.set_subset)) if elem in self.set_subset[subset_no]  ] for elem in self.ground_set] 
        self.max_frequency=max([sum([subset.count(elem) for subset in self.set_subset]) for elem in self.ground_set])
        #print(self.frequency_list[0])


    #def bit_mask_solver(self,covered_mask,now_consider_index):
        
    def subset_bit_mask_maker(self):
        
        for subset_no in range(self.total_subset):
            mask=0
            for element_no in range(self.total_element):
                if(self.ground_set[element_no] in self.set_subset[subset_no]):
                  mask= mask | (1<<element_no)
                  
            self.subset_mask.append(mask)
            
        #print(self.subset_mask)

    def bit_mask_solver(self):

        self.lp_result=[]
        self.cost=0.0
        
        self.subset_bit_mask_maker()
        mask_weight = []
        idx=[]
        
        for count in range(1<<self.total_element):
            mask_weight.append(float("inf"))

        for count in range(1<<self.total_element):
            idx.append(0)
            
        mask_weight[0]=0.0

        min_cost = float("inf")

        for subset_count in range(self.total_subset):
            for set_count in range(1<<self.total_element):
                #print(mask_weight)
                if(mask_weight[set_count]==float("inf")):
                    continue;
                if(mask_weight[set_count | self.subset_mask[subset_count]]==float("inf") ):
                    mask_weight[set_count | self.subset_mask[subset_count]]=mask_weight[set_count]+self.weight[subset_count]
                    if(set_count==0.0):
                        idx[self.subset_mask[subset_count]]=1<<subset_count
                    else:
                        idx[set_count | self.subset_mask[subset_count]]=idx[set_count] | 1<<subset_count
                        
                else:
                    if(mask_weight[set_count | self.subset_mask[subset_count]] > mask_weight[set_count]+self.weight[subset_count]):
                        mask_weight[set_count | self.subset_mask[subset_count]]=mask_weight[set_count]+self.weight[subset_count]
                        idx[set_count | self.subset_mask[subset_count]]=idx[set_count] | 1<<subset_count
                        
            if(mask_weight[(1<<self.total_element)-1]!=float("inf")):
                min_cost=min(min_cost,mask_weight[(1<<self.total_element)-1])

        self.cost=min_cost
        #print(min_cost)
        subsetSequence=idx[(1<<self.total_element)-1]

        for subset_count in range(self.total_subset):
            if(subsetSequence & 1<<subset_count):
                self.lp_result.append(subset_count)

        return (self.lp_result,self.cost)
        
                    
            
            
        
            

#file_name= 'test_generate.txt'
#file_name='test_data.txt'
#file_name='testcase_generate.txt'
file_name='testcase1_generate.txt'

with open(file_name) as reader:
    ints_ = [float(i) for i in reader.read().split()]

#print(ints_)

iterator = iter(ints_)

test_case = int(next(iterator))

#print(test_case)
lp_time=[]
bitmask_time=[]
lp_cost=[]
bitmask_cost=[]
final_data=[]
row=['no.elem','lp_time','bitmask_time','approx.']
final_data.append(row)

for test_no in range(test_case):
    print("Test Case :: %d " % (test_no+1))
    problem={}
    total_ground_element= int(next(iterator))
    total_subset = int(next(iterator))
    set_subset=[ [] for subset in range(total_subset) ]
    weight=[]
    for subset_no in range(total_subset):
        weight.append(next(iterator))
        no_element= int(next(iterator))
        for element in range(no_element):
            set_subset[subset_no].append(int(next(iterator)))

    problem["total_element"]=total_ground_element
    problem["total_subset"]=total_subset
    problem["set_subset"]=set_subset
    problem["weight"]=weight

    
    set_cov= Set_Cover(problem)
    set_cov.problem_formulate()
    start_time=time.time()
    ids,cost=set_cov.lp_solver()
    #set_cov.bit_mask_solver(0,0)
    #set_cov.print_bit_mask()
    print("\nLinear Programming Solution----")
    print("_________________________________")
    print("IDS:: ")
    print([(i+1) for i in ids])
    print("Cost :: %.2f" %cost)
    print("\n")
    print("\nBitmask Solution----")
    print("_________________________________")
    end_time=time.time()
    lp_time.append(end_time-start_time)
    start_time=time.time()
    lp_cost.append(cost)
    #set_cov.subset_bit_mask_maker()
    ids,cost=set_cov.bit_mask_solver()  
    print("IDS:: ")
    print([(i+1) for i in ids])
    print("Cost :: %.2f" %cost)
    print("\n\n")
    end_time=time.time()
    bitmask_time.append(end_time-start_time)
    bitmask_cost.append(cost)
    row=[]
    row.append(total_ground_element)
    row.append(lp_time[-1])
    row.append(bitmask_time[-1])
    row.append(lp_cost[-1]/bitmask_cost[-1])
    final_data.append(row)
#print(bitmask_time)
#print(lp_time)
#print(bitmask_cost)
#print(lp_cost)


with open('G:\\report.csv', 'w',newline='') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    
    for row in final_data:
        thedatawriter.writerow(row)
