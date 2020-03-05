import util, plot, features
from util import rng
import kappy
from copy import deepcopy

from params import params

def main():
	if params['experiment'] == 'hist':
		hist()
	elif params['experiment'] == 'sweep':
		sweep()
	else: 
		assert(False) #unknown 'experiment' param

	print("\n\n Done. \n\n")


############################################### EXPERIMENTS ###############################################

def hist():
	print("\nComparing two simulations using histogram.\n")
	# compares 2 runs, no averaging
	NADs = [1.0E+4,1.0E+5]
	labels = ['[NAD] = ' + str(NADs[0]), '[NAD] = ' + str(NADs[1])]

	all_params = []
	feature_names = ['size', 'branching ratio']

	shots = []
	data = {n:[] for n in feature_names}
	for i in rng(NADs):
		params['NAD'] = NADs[i]
		sshot = run_sim(params)
		for feat in feature_names:
			data[feat] += [features.extract_one(feat, sshot)]
		all_params += [params]
		
	util.pickle_it(all_params, data) 

	plot.hist_first_and_last(data,params,feature_names, labels) # 1 img per feature




def sweep():
	# compares many parameters and averages each over many runs
	print("\nRunning parameter sweep with repeats.\n")
	#NADs = [(5**i) for i in range(2,6)]
	PARGs = [(2**i) for i in range(1,6)]
	all_params = []

	feature_names = ['size', 'branching ratio']

	stats = {'avg':[], 'std':[],'top1':[], 'top2':[],'top3':[], 'btm1':[],'btm2':[],'btm3':[]}
	merged_data = {n:{'avg':deepcopy(stats), 'max':deepcopy(stats), 'iod':deepcopy(stats),'1:2':deepcopy(stats)} for n in feature_names}


	shots = []
	for i in rng(PARGs):
		#params['NAD'] = NADs[i]
		#print("[NAD] = ",NADs[i])
		params['PARG'] = PARGs[i]
		print("[PARG] = ",PARGs[i])
		repeats_data = {n:{'avg':[], 'max':[], 'iod':[],'1:2':[]} for n in feature_names}
		# Format: data[feature_name][stat]. Example: data['size']['avg']

		for r in range(params['repeats']):

			sshot = run_sim(params)
			features.extract_stats(repeats_data, feature_names,sshot)

		features.merge_repeats(merged_data, repeats_data, feature_names)
		all_params += [params]
		
	util.pickle_it(all_params, merged_data) 

	#plot.param_sweep(merged_data,params,NADs,'[NAD]',feature_names) #features * stats imgs
	plot.param_sweep(merged_data,params,PARGs,'[PARG]',feature_names) #features * stats imgs


###################################### KAPPY ###############################################

def run_sim(params):
	client = kappy.KappaStd()

	with open('base_model.ka', 'r') as file : 
		model = file.read()

	for species in ['NAD','DNA','PARP','PARG']:
		model = model.replace("init: _ " + species, "init: " + str(params[species]) + " " + species)

	for rate in ['base_rev','base_fwd','catalysis_rate','cut_rate']:
		model = model.replace("'" + rate + "' _", "'" + rate + "' " + str(params[rate]))

	model = model.replace("mod: ([E] [mod] _ )=0", "mod: ([E] [mod] " + str(params['time']/100) + " )=0")

	client.add_model_string(model)
	client.project_parse()
	sim_params = kappy.SimulationParameter(pause_condition="[T] > " + str(params['time']),plot_period=params['time']/10)
	client.simulation_start(sim_params)
	client.wait_for_simulation_stop()
	results = client.simulation_plot()
	snaps = client.simulation_snapshots()
	snap  = client.simulation_snapshot(snaps['snapshot_ids'][0])

	#for i in rng(snaps['snapshot_ids']):
	#	snap  = client.simulation_snapshot(snaps['snapshot_ids'][i])
	#	if snap != []:
	#		break

	client.simulation_delete()
	client.shutdown()

	return snap

main()