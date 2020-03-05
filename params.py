import util 

params = ({'experiment':'sweep', 'repeats':20, 'time':100000, 'timestamp':util.timestamp(), 
	'NAD':10000, 'PARG':0, 'DNA': 20, 'PARP':20,
	'base_fwd':1.0E+2, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+5, 'cut_rate':1.0E-8,
	'out_dir':'./output/local/', 'write_params_on_img':False, 'save_fig':True, 'dpi':300, 'std_devs':1})

assert(params['std_devs']==1) # removed support for other values


# prev
#params = ({'experiment':'sweep', 'repeats':20, 'time':100000, 'timestamp':util.timestamp(), 
#	'NAD':10000, 'PARG':0, 'DNA': 20, 'PARP':20,
#	'base_fwd':1.0E+4, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+8, 'cut_rate':1.0E-8,
#	'out_dir':'./output/local/', 'write_params_on_img':False, 'save_fig':True, 'dpi':300, 'std_devs':1})
