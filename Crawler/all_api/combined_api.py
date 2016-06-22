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
from startupsclub_api import maindic_startupsclub
from eventful_api import maindic_eventful
from eventBrite_api import maindic_eventBrite
from meetup_api import maindic_meetup
from Graph_api import maindic_Graph
from eventsHigh_api import maindic_eventsHigh
from allevents_api import maindic_allevents
all_dics=[maindic_eventful,maindic_meetup,maindic_startupsclub,maindic_eventBrite,maindic_eventsHigh,maindic_allevents,maindic_Graph]
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
with open('events.json', 'w') as outfile:
	json.dump(main_dic, outfile,ensure_ascii=False)