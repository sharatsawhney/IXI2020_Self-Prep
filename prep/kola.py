import math


class Evaluate:
	def logistic_model(item_params , thetas1):
		#getting all tags filtered..
		ref = {}
		ques_ids = []
		tag_sep = {}
		As = {}
		Bs = {}
		Us = {}
		for i in item_params:
			ques_ids.append(i["q_id"])
			ref[i["q_id"]] = [i["t_id"],i["a"],i["b"],i["u"]]

			if i["t_id"] in tag_sep:
				tag_sep[i["t_id"]].append(i["q_id"])
			else:
				tag_sep[i["t_id"]] = [i["q_id"]]

			if i["t_id"] in As:
				As[i["t_id"]].append(i["a"])
			else:
				As[i["t_id"]] = [i["a"]]

			if i["t_id"] in Bs:
				Bs[i["t_id"]].append(i["b"])
			else:
				Bs[i["t_id"]] = [i["b"]]

			if i["t_id"] in Us:
				Us[i["t_id"]].append(i["u"])
			else:
				Us[i["t_id"]] = [i["u"]]

		thetas = {}
		for i in thetas1:
			thetas[i["t_id"]] = i["theta"]

		thets = []
		# print(As)
		# print(Bs)
		# print(Us)
		# print(thetas)
		for i in tag_sep:
			loss = 10**6
			thet_0 = thetas[i]
			a = As[i]
			b = Bs[i]
			u = Us[i]
			while loss>0.001 or loss <-0.001:
				pthet = []
				# print(thet_0,a,b,u)
				for ai,bi in zip(a,b):
					pthet.append(1/(1+math.exp(-ai*(thet_0-bi))))
				sume1 = 0
				sume2 = 0
				# print(pthet)
				for ai,ui,pi in zip(a,u,pthet):
					sume1 += ai*(ui-pi)
					sume2 += ai*ai*pi*(1-pi)
				# print(sume1,sume2)
				thet_1 = thet_0 + sume1/float(sume2)
				if thet_1>=-3 and thet_1<=3:
					loss = sume1/float(sume2)
					thet_0 = thet_1
				else:
					loss = -3
					if thet_1>3:
						thet_0 = 3
					else:
						thet_0 = -3
				# print(loss)
			thets.append({i:thet_0})
		return thets

# inp1 = [{"q_id":1,"t_id":1,"a":1.0,"b":-1,"u":1},{"q_id":2,"t_id":1,"a":1.2,"b":0,"u":0},{"q_id":3,"t_id":1,"a":0.8,"b":1,"u":1},
# 		{"q_id":4,"t_id":2,"a":2,"b":-2,"u":1},{"q_id":5,"t_id":2,"a":1,"b":-2,"u":0},{"q_id":6,"t_id":2,"a":0,"b":0,"u":0}]

# inp2 = [{"t_id":1,"theta":-1},{"t_id":2,"theta":2}]

# print(logistic_model(inp1,inp2))