import util, plot
from util import rng
import numpy as np, scipy.stats as st


def extract_one(feature, sshot):
	if name == 'size':
		feat = ['some','fn','of','sshot']
	elif name == 'branching ratio':
		feat = []
	else: 
		assert(False) #feature name not recognized

	return feat

def extract_stats(data, feature_names, sshot):
	for name in feature_names:
		feat = extract_one(name, sshot)

		data[name]['avg'] += [util.avg(feat)]
		if util.avg != 0:
			iod = util.var(feat)/util.avg(feat)
		else:
			iod = 0
		data[name]['iod'] += [iod]
		max1 = max(feat)
		feat.remove(max1)
		max2 = max(feat)
		data[name]['max'] += [max1]

		if max1==0:
			ratio = 0
		else: 
			ratio = (max1 - max2)/max1
		data[name]['1:2'] += [ratio]


def merge_repeats(merged_data, repeats_data, feature_names):
	for name in feature_names:
		for metrics in repeats_data[name].keys():

			merged_data[name][metric]['avg'] = util.avg(repeats_data[name][metric])

			a = np.array(repeats_data[name][metric])
			mean = np.mean(a)
			merged_data[name][metric]['avg'] = mean


			conf_interval1 = st.t.interval(0.68, len(a)-1, loc=mean, scale=st.sem(a)) #1 standard devs
			conf_interval2 = st.t.interval(0.95, len(a)-1, loc=mean, scale=st.sem(a)) #2 standard devs
			conf_interval3 = st.t.interval(0.997, len(a)-1, loc=mean, scale=st.sem(a)) #3 standard devs

			intervals, stats = [conf_interval1, conf_interval2, conf_interval3], [['top1','btm1'],['top2','btm2'],['top3','btm3']]
			for i in util.rng(intervals):
				interval, stat = intervals[i], stats[i]:
				a_trim=a[a>interval[0]]
				a_trimd=a_trim[a_trim<interval[1]]
				if np.count_nonzero(a_trimd) == 0:
					conf_min, conf_max = 0,0
				else:
					conf_min, conf_max = a_trimd.min(), a_trimd.max()
				merged_data[name][metric][stat[0]] = conf_max
				merged_data[name][metric][stat[1]] = conf_min


