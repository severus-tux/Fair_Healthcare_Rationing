import numpy as np

class VaccineAllocInstance:
	def __init__(self,n,c,d,q,availability,belongsToCatagory,Q_d,Q_c,Q_cxd,U_nxd):
		self.n = n #Number of agents
		self.c = c #Number of catagories
		self.d = d #Numenr of days
		self.q = q #Total Vaccines
		self.availability = availability
		self.belongsToCatagory = belongsToCatagory
		self.Q_d = Q_d
		self.Q_c = Q_c
		self.Q_cxd = Q_cxd
		self.U_nxd = U_nxd


	# def print_instance(self):
	# 	print("Number of agents: ",self.n)
	# 	print("Number of catagories: ",self.c)
	# 	print("Number of days: ",self.d)
	# 	print("Total quota: ",self.q)
	# 	print("Daily quotas:",self.Q_d)
	# 	print("catagory quota: ",self.Q_c)
	# 	print("CatagoryxDaily quota:\n",np.matrix(self.Q_cxd))
	# 	print("Availability:\n",np.matrix(self.availability))
	# 	print("belongsToCatagory:\n",np.matrix(self.belongsToCatagory))
	# 	print("Utility:\n",np.matrix(self.U_nxd))
	# 	print("Single delta value:",self.delta)