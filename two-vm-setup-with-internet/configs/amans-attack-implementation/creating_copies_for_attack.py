import yaml
from copy import deepcopy

no_of_ue = 25
base_supi = "imsi-999700000000001"
with open('config/open5gs-ue.yaml', 'r') as file:
	original_ue = yaml.safe_load(file)

print(original_ue)

att_ue = int(base_supi.split('-')[1])
new_ue = deepcopy(original_ue)

for i in range(1,no_of_ue+1):
	new_ue['supi'] = "imsi-"+ str(att_ue + i)
	with open('config/open5gs-ue'+ str(1+i) +'.yaml', 'w') as file:
		yaml.dump(new_ue, file)


