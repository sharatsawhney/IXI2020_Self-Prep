import pandas as pd 
import numpy as np 
from collections import OrderedDict

corr = pd.read_csv("C:/Users/pratyush/Downloads/corr1.csv",index_col = 0)
start = 0
leve = 0
curr = -1
curr_lev_sorted = []
completed_pars = {}

def saturate(thres):
	if thres<=2.5:
		return False
	else:
		return True

# run each time the student has taken a assignment..
def get_path(theta1,levels,parents,threshold=2.5):
	global start,leve,curr,curr_lev_sorted,completed_pars
	theta = {}
	inv_th = {}
	for i in theta1:
		theta[i["t_id"]] = i["theta"]
		inv_th[i["theta"][-1]] = i["t_id"]
	sort_t = sorted(list(inv_th.keys()))

	# if starts.. at level 0..
	if leve==0 and start==0:
		start = 1
		thet0 = dict([(theta[i][-1],i) for i in levels[0]])
		curr_lev_sorted = sorted(list(thet0.keys()))
		curr_lev_sorted = [thet0[i] for i in curr_lev_sorted]
		curr = curr_lev_sorted[-1]
		curr_lev_sorted = curr_lev_sorted[:-1]

	elif leve>=0 and start==1:
		if saturate(theta[curr][-1]) and len(curr_lev_sorted)==0:
			completed_pars[curr] = (theta[curr][-1]-theta[curr][0])/theta[curr][0]
			leve += 1
			thet1 = dict([(theta[i][-1],i) for i in levels[leve]])
			thet2 = dict([(i,theta[i][-1]) for i in levels[leve]])
			thet2 = {k: v for k, v in sorted(thet2.items(), key=lambda item: item[1],reverse = True)}
			pars = {}
			for i in levels[leve]:
				for j in parents[i]:
					if i in pars:
						pars[i] += completed_pars[j]
					else:
						pars[i] = completed_pars[j]

			pars = {k: v for k, v in sorted(pars.items(), key=lambda item: item[1],reverse = True)}
			
			prev = list(pars.values())[0]
			prev_k =list(pars.keys())[0]
			sort = [list(pars.keys())[0]]

			for i,j in zip(list(pars.keys())[1:],list(pars.values())[1:]):
				if j==prev:
					temp = [prev_k]
					while j==prev:
						temp.append(i)
					for k,o in zip(list(temp.keys()),list(temp.values())):
						print(k,o)
						if k in temp:
							sort.append(k)
				else:
					sort.append(i)

			curr_lev_sorted = sort
			curr = curr_lev_sorted[-1]
			curr_lev_sorted = curr_lev_sorted[:-1]
			

		elif saturate(theta[curr][-1]) and len(curr_lev_sorted)!=0:
			completed_pars[curr] = (theta[curr][-1]-theta[curr][0])/theta[curr][0]
			curr = curr_lev_sorted[-1]
			curr_lev_sorted = curr_lev_sorted[:-1]
		else:
			print("continue...")


# run only once
def pathfinder():
	# make the graph..
	corr.columns = [int(i) for i in corr.columns]
	corr.index = [int(i) for i in corr.index]
	tags = list(corr.columns)
	queue = []
	levels = {}
	parents = {}

	# parents immediate..
	for i in corr.columns:
		for j,k in zip(corr.index,corr[i]):
			if k==1:
				if i in parents:
					parents[i].append(j)
				else:
					parents[i]=[j]

	# init the levels..
	for i in tags:
		levels[i] = 0
	
	# find the level zero nodes..
	queue.extend(list(corr.columns[(corr == 0).all()]))
	while len(queue)>0:
		node = queue[0]
		queue = queue[1:]
		lev = levels[node]

		df = corr==1
		df = df.ix[node]
		df = list(df[df].index)
		for i in df:
			levels[i] = lev + 1
			queue.append(i)

	return levels,parents

inp0 = [{"t_id":1,"theta":[1.2,1.3,1.2]},{"t_id":2,"theta":[1.3,1.2,1.5]}
			,{"t_id":3,"theta":[0.6,1.1,1.2]},{"t_id":4,"theta":[1.4,1.8,2.1]}
			,{"t_id":5,"theta":[1.7,1.8,2.0]},{"t_id":6,"theta":[2.1,2.3,2.5]}
			,{"t_id":7,"theta":[1.5,1.7,2.3]}]

inp1 = [{"t_id":1,"theta":[1.2,1.3,1.2]},{"t_id":2,"theta":[1.3,1.2,1.5]}
			,{"t_id":3,"theta":[0.6,1.1,1.2]},{"t_id":4,"theta":[1.4,1.8,2.1]}
			,{"t_id":5,"theta":[1.7,1.8,2.0]},{"t_id":6,"theta":[2.1,2.3,2.5]}
			,{"t_id":7,"theta":[1.5,1.7,2.3,2.4,2.4,2.4]}]

inp2 = [{"t_id":1,"theta":[1.2,1.3,1.2]},{"t_id":2,"theta":[1.3,1.2,1.5]}
			,{"t_id":3,"theta":[0.6,1.1,1.2]},{"t_id":4,"theta":[1.4,1.8,2.1]}
			,{"t_id":5,"theta":[1.7,1.8,2.0]},{"t_id":6,"theta":[2.1,2.3,2.5]}
			,{"t_id":7,"theta":[1.5,1.7,2.3,2.4,2.4,2.4,2.6,2.8,2.7]}]

inp3 = [{"t_id":1,"theta":[1.2,1.3,1.2,2.0,2.4,2.6]},{"t_id":2,"theta":[1.3,1.2,1.5]}
			,{"t_id":3,"theta":[0.6,1.1,1.2]},{"t_id":4,"theta":[1.4,1.8,2.1]}
			,{"t_id":5,"theta":[1.7,1.8,2.0]},{"t_id":6,"theta":[2.1,2.3,2.5]}
			,{"t_id":7,"theta":[1.5,1.7,2.3,2.4,2.4,2.4,2.6,2.8,2.7]}]

# inp1 = [{"t_id":1,"theta":[1.2,1.3,1.2,2.0,2.4,2.6]},{"t_id":2,"theta":[1.3,1.2,1.5]}
# 			,{"t_id":3,"theta":[0.6,1.1,1.2]},{"t_id":4,"theta":[1.4,1.8,2.1]}
# 			,{"t_id":5,"theta":[1.7,1.8,2.0]},{"t_id":6,"theta":[2.1,2.3,2.5]}
# 			,{"t_id":7,"theta":[1.5,1.7,2.3,2.6,2.8,2.7]}]

levels1,parents = pathfinder()
levels = {}
for i in levels1:
	if levels1[i] in levels:
		levels[levels1[i]].append(i)
	else:
		levels[levels1[i]] = [i]

print(levels)
#first run...
get_path(inp0,levels,parents)
print(curr)
print(leve)
print(curr_lev_sorted)

get_path(inp1,levels,parents)
print(curr)
print(leve)
print(curr_lev_sorted)

get_path(inp2,levels,parents)
print(curr)
print(leve)
print(curr_lev_sorted)

get_path(inp3,levels,parents)
print(curr)
print(leve)
print(curr_lev_sorted)
		