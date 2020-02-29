import util, plot
from util import rng


# TODO: 
# lots of debug
# merge sams part
# pickle more raw data, also need to pass the varied param somehow
# Add README
# params -> ka

params = ({'experiment':'hist', 'repeats':10, 
	'out_dir':'./output/', 'write_params_on_img':True, 'save_fig':False})



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
	NADs = [10,10000]

	feature_names = ['size', 'branching ratio']

	shots = []
	data = {n:[] for n in feature_names}
	for nad in NADs:
		params['NAD'] = nad
		sshot = run_sim(params)
		for feat in feature_names:
			data[feat] += [features.extract_one(feat, sshot)]
		
	util.pickle_it(data, params) 

	plot.hist_first_and_last(data,params,feature_names) # 1 img per feature




def sweep():
	# compares many parameters and averages each over many runs
	print("\nRunning parameter sweep with repeats.\n")
	NADs = [10**i for i in range(4)]

	feature_names = ['size', 'branch ratio']

	stats = {'avg':[], 'top1':[], 'top2':[],'top3':[], 'btm1':[],'btm2':[],'btm3':[]}
	merged_data = {n:{'avg':stats.copy(), 'max':stats.copy(), 'iod':stats.copy(),'1:2':stats.copy()} for n in feature_names}


	shots = []
	for i in rng(NADs):
		params['NAD'] = NADs[i]
		repeats_data = {n:{'avg':[], 'max':[], 'iod':[],'1:2':[]} for n in feature_names}
		# Format: data[feature_name][stat]. Example: data['size']['avg']

		for r in rng(params['repeats']):

			sshot = run_sim(params)
			features.extract_stats(repeats_data, feature_names)
		features.merge_repeats(merged_data, repeats_data, feature_names)
		
	util.pickle_it(merged_data, params) 

	plot.param_sweep(merged_data,params,NADs,'NAD',feature_names) #features * stats imgs



main()