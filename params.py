import util 

params = ({'experiment':'sweep', 'repeats':8, 'time':100, 'timestamp':util.timestamp(), 
	'NAD':1000, 'PARG':0, 'DNA': 20, 'PARP':20,
	'base_fwd':1.0E+2, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+8, 'cut_rate':1.0E-8,
	'out_dir':'./output/local/', 'write_params_on_img':False, 'save_fig':False, 'dpi':100, 'std_devs':1})

assert(params['std_devs']==1) # removed support for other values