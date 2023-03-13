from pulp import *
import sys
import os
import copy
import numpy as np
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from vaccine_alloc_instance_df import *
from allocation_solution_df import *
	
class LPOfflineMaxUtility:
	def __init__(self, vaccine_obj):
		self.vaccine_obj = copy.deepcopy(vaccine_obj)

	def solve(self):
		## BEGIN: PreSetup LP

		days = ["d_"+str(i) for i in range(self.vaccine_obj.d)]
		catagories = ["c_"+str(i) for i in range(self.vaccine_obj.c)]
		catagory_nodes = ["c_"+str(i)+"_"+str(j) for i in range(self.vaccine_obj.d) for j in range(self.vaccine_obj.c)]
		agents = ["a_"+str(i) for i in range(self.vaccine_obj.n)]

		# list of nodes
		nodes = ["s","v"]+days+catagory_nodes+agents+["t"]

		# supply or demand of nodes
		            #NodeID : [Supply,Demand]
		nodeData = {x:[0,0] for x in nodes}
		nodeData["s"] = [self.vaccine_obj.q,0]
		nodeData["t"] = [0,self.vaccine_obj.q]

		# Arcs List
		arcs = [("s","v")]
		for i in days:
			arcs.append(("v",i))

		for i in range(self.vaccine_obj.d):
			for j in range(self.vaccine_obj.c):
				arcs.append(("d_"+str(i),"c_"+str(i)+"_"+str(j)))

		for i in range(self.vaccine_obj.n):
			for j in range(self.vaccine_obj.d):
				if (self.vaccine_obj.availability[i][j]==1):
					for k in range(self.vaccine_obj.c):
						if (self.vaccine_obj.belongsToCatagory[i][k]):
							arcs.append(("c_"+str(j)+"_"+str(k),"a_"+str(i)))

		for i in agents:
			arcs.append((i,"t"))

		#Arcs Data
		# arcs cost, lower bound and capacity
		   		#Arc : [Cost,MinFlow,MaxFlow]
		arcData = {("s","v"):[0,0,self.vaccine_obj.q]}
		for i in range(self.vaccine_obj.d):
			arcData[("v","d_"+str(i))]=[0,0,self.vaccine_obj.Q_d[i]]

		for i in range(self.vaccine_obj.d):
			for j in range(self.vaccine_obj.c):
				arcData[("d_"+str(i),"c_"+str(i)+"_"+str(j))]=[0,0,self.vaccine_obj.Q_cxd[j][i]]

		for i in range(self.vaccine_obj.n):
			for j in range(self.vaccine_obj.d):
				if (self.vaccine_obj.availability[i][j]==1):
					for k in range(self.vaccine_obj.c):
						if (self.vaccine_obj.belongsToCatagory[i][k]):
							arcData[("c_"+str(j)+"_"+str(k),"a_"+str(i))]=[self.vaccine_obj.U_nxd[i][j],0,1]

		for i in agents:
			arcData[(i,"t")]=[0,0,1]

		# Splits the dictionaries to be more understandable
		(supply, demand) = splitDict(nodeData)
		(costs, mins, maxs) = splitDict(arcData)

		## END: PreSetup LP

		## BEGIN: Setup LP
		# Creates the boundless Variables as Continues_valued_variables
		vars = LpVariable.dicts("Route",arcs,None,None,cat='Continuous')#LpInteger)

		# Creates the upper and lower bounds on the variables
		for a in arcs:
		    vars[a].bounds(mins[a], maxs[a])

		##LP
		# Creates the 'prob' variable to contain the problem data    
		prob = LpProblem(name="Offline_max_Utility",sense=LpMaximize)

		# Creates the objective function
		obj = [vars[a]* costs[a] for a in arcs[1:]]
		prob += lpSum(obj), "Total Cost of Transport"

		# Creates all problem constraints - this ensures the amount going into each node is equal to the amount leaving


		for k in nodes[1:-1]: #Except for last node node t and first node s
		    prob += (supply[k]+ lpSum([vars[(i,j)] for (i,j) in arcs if j == k]) ==
		             demand[k]+ lpSum([vars[(i,j)] for (i,j) in arcs if i == k])), \
		            "Flow Conservation in Node %s"%k

		# Category quota constraints
		for c_i in range(self.vaccine_obj.c):
			prob += (lpSum([vars[("d_"+str(d_j),"c_"+str(d_j)+"_"+str(c_i))] for d_j in range(self.vaccine_obj.d)])  <=
				self.vaccine_obj.Q_c[c_i] ), \
			"catagory quota for C_%s"%c_i

		# The problem data is written to an .lp file
		# prob.writeLP("simple_MCFP.lp")

		## END: Setup LP

		# The problem is solved using PuLP's choice of Solver
		prob.solve()#GLPK(msg = 0))

		sol = AllocationSolution(self.vaccine_obj.n,self.vaccine_obj.d)
		sol.status = prob.status
		sol.total_flow = value(vars[("s","v")])

		for i in range(self.vaccine_obj.n):
			for j in range(self.vaccine_obj.d):
				if (self.vaccine_obj.availability[i][j]==1):
					for k in range(self.vaccine_obj.c):
						if (self.vaccine_obj.belongsToCatagory[i][k]):
							if ((value(vars[("c_"+str(j)+"_"+str(k),"a_"+str(i))]))==1.0):
								sol.Allocation[i][j]=k
								sol.total_utility += self.vaccine_obj.U_nxd[i][j]

		
		return sol
