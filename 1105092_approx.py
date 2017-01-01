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
    
