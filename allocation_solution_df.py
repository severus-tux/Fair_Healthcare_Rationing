class AllocationSolution:
	def __init__(self,n,d):
		self.Allocation = [[-1 for j in range(d)] for i in range(n)]
		self.total_flow = 0
		self.total_utility = 0
		self.status = "Not Solved"
		self.solutionTime=0
