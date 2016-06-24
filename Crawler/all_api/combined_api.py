import json
all_cities=[]

main_dic={}
apis=['eventfulApi','eventBriteApi','meetupApi','startupsclub','eventsHigh','allevents','Graph_Api']

with open('details.json') as basic_details:
	d = json.load(basic_details)
	for api in apis:
		cities=d[api]['cities']
		for city in cities:
			if city in all_cities:
				pass
			else:
				all_cities.append(city)	

print all_cities  
all_dics=[]
try:
	from startupsclub_api import maindic_startupsclub
	all_dics.append(maindic_startupsclub)
except ImportError:
	print "startupsclub error "
try:
	from eventful_api import maindic_eventful
	all_dics.append(maindic_eventful)
except ImportError:
	print "eventful error"
try:
	from eventBrite_api import maindic_eventBrite
	all_dics.append(maindic_eventBrite)
except ImportError:
	print "eventBrite error"
try:
	from meetup_api import maindic_meetup
	all_dics.append(maindic_meetup)
except ImportError:
	print "meetup error"
try:		
	from Graph_api import maindic_Graph
	all_dics.append(maindic_Graph)
except ImportError:
	print "Graph error"
try:
	from eventsHigh_api import maindic_eventsHigh
	all_dics.append(maindic_eventsHigh)
except ImportError:
	print "eventsHigh error"
'''try:
	from allevents_api import maindic_allevents
	all_dics.append(maindic_allevents)
except ImportError:
	print "allevents error"	'''

for city in all_cities:
	all_events=[]
	duplicate=0
	for dics in all_dics:
		if city in dics:
			for ind_event in dics[city]:
				ind_event_name=ind_event['name']
				if ind_event_name is None:
					ind_event_name="None"

				if any(ind_event_name in s['name'] for s in all_events):
					print ind_event_name
					duplicate=duplicate+1
					dics[city].remove(ind_event)
			all_events=all_events+dics[city]
	main_dic[city]=all_events
	print " ***********************"+ "  "+str(duplicate)
	with open('events_'+city+'.json', 'w') as outfile:
		json.dump(main_dic[city], outfile,ensure_ascii=False)

with open('events.json', 'w') as outfile:
	json.dump(main_dic, outfile,ensure_ascii=False)