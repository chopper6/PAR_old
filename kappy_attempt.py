import kappy

client = kappy.KappaStd()

with open('base_model.ka', 'r') as file : 
	model = file.read()

client.add_model_string(model)
client.project_parse()
sim_params = kappy.SimulationParameter(pause_condition="[T] > " + str(params['iterations']),plot_period=1)
client.simulation_start(sim_params)
client.wait_for_simulation_stop()
results = client.simulation_plot()
snaps = client.simulation_snapshots()
snap  = client.simulation_snapshot(snaps['snapshot_ids'][0])
client.simulation_delete()
client.shutdown()

def get_branch_number(graph) :
	counter = 0
	for agent in graph[1] :
		for node_site in agent['node_sites']:
			if node_site['site_name'] == 'branch' and node_site['site_type'][1]['port_links'] :
				#if branch site is not empty
				counter +=1
	return counter

def get_infos(snap) :
	graphs = snap['snapshot_agents']
	infos = [] 
	for graph in graphs : #run through the graphs
		if graph[1][0]['node_type'] == 'PARG' :
			continue
		info = {}
		info['size'] = len(graph[1]) # number of agents
		info['number'] = graph[0] #number of that kind of graph
		info['branching_ratio'] = get_branch_number(graph)/info['size']
		infos.append(info)
	return infos
#print(snap)
#print(len(snap['snapshot_agents'][0][1]))
get_infos(snap)

