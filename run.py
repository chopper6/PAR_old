import util, plot, features
from util import rng
import kappy
from copy import deepcopy


params = ({'experiment':'hist', 'repeats':10, 'time':100, 'timestamp':util.timestamp(), 
	'NAD':1000, 'PARG':200, 'DNA': 20, 'PARP':20,
	'base_fwd':1.0E+8, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+8, 'cut_rate':1.0E-8, 'elong_boost':1.0E+1,
	'out_dir':'./output/', 'write_params_on_img':True, 'save_fig':False, 'dpi':300, 'std_devs':3})


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
	NADs = [1000,10000]

	all_params = []
	feature_names = ['size', 'branching ratio']

	shots = []
	data = {n:[] for n in feature_names}
	for nad in NADs:
		params['NAD'] = nad
		sshot = run_sim(params)
		for feat in feature_names:
			data[feat] += [features.extract_one(feat, sshot)]
		all_params += [params]
		
	util.pickle_it(all_params, data) 

	plot.hist_first_and_last(data,params,feature_names) # 1 img per feature




def sweep():
	# compares many parameters and averages each over many runs
	print("\nRunning parameter sweep with repeats.\n")
	NADs = [10**i for i in range(4)]
	all_params = []

	feature_names = ['size', 'branching ratio']

	stats = {'avg':[], 'top1':[], 'top2':[],'top3':[], 'btm1':[],'btm2':[],'btm3':[]}
	merged_data = {n:{'avg':deepcopy(stats), 'max':deepcopy(stats), 'iod':deepcopy(stats),'1:2':deepcopy(stats)} for n in feature_names}


	shots = []
	for i in rng(NADs):
		params['NAD'] = NADs[i]
		repeats_data = {n:{'avg':[], 'max':[], 'iod':[],'1:2':[]} for n in feature_names}
		# Format: data[feature_name][stat]. Example: data['size']['avg']

		for r in range(params['repeats']):

			sshot = run_sim(params)
			features.extract_stats(repeats_data, feature_names,sshot)

		features.merge_repeats(merged_data, repeats_data, feature_names)
		all_params += [params]
		
	util.pickle_it(all_params, merged_data) 

	plot.param_sweep(merged_data,params,NADs,'NAD',feature_names) #features * stats imgs


###################################### KAPPY ###############################################

def run_sim(params):
	client = kappy.KappaStd()

	with open('base_model.ka', 'r') as file : 
		model = file.read()

	for species in ['NAD','DNA','PARP','PARG']:
		model = model.replace("init: _ " + species, "init: " + str(params[species]) + " " + species)

	for rate in ['base_rev','base_fwd','catalysis_rate','cut_rate','elong_boost']:
		model = model.replace("'" + rate + "' _", "'" + rate + "' " + str(params[rate]))

	model = model.replace("mod: ([E] [mod] _ )=0", "mod: ([E] [mod] " + str(params['time']) + " )=0")

	client.add_model_string(model)
	client.project_parse()
	sim_params = kappy.SimulationParameter(pause_condition="[T] > " + str(params['time']),plot_period=params['time'])
	client.simulation_start(sim_params)
	client.wait_for_simulation_stop()
	results = client.simulation_plot()
	snaps = client.simulation_snapshots()
	snap  = client.simulation_snapshot(snaps['snapshot_ids'][0])
	client.simulation_delete()
	client.shutdown()

	return snap

main()