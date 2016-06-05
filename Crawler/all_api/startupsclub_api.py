import urllib2
import json
import httplib
from pprint import pprint
import datetime
import time

cities=[]
with open('details.json') as basic_details:    
	d = json.load(basic_details)
	cities=d['startupsclub']['cities']
	token=d['startupsclub']['token']
	api_url=d['startupsclub']['url']
print cities 

for city in cities:
	events=[]

	if city in ("Bangalore","bangalore","Bengaluru","bengaluru"):
		search_char1="BLR"
	  	search_char2="Bangalore"
	elif city in ("mumbai","Mumbai"):
	  	search_char1="MUM"
	  	search_char2="Mumbai"
	elif city in ("Chennai","chennai"):
	  	search_char1="CHE"
	  	search_char2="Chennai"
	elif city in ("Pune","pune"):
	  	search_char1="PUNE"
	  	search_char2="Pune"
	elif city in("Hyderabad","hyderabad"):
	  	search_char1="HYD"
	  	search_char2="Hyderabad"
	elif city in ("Ahmedabad","ahmedabad"):
	  	search_char1="AHD"
	  	search_char2="Ahmedabad"
	elif city in ("Visakhapatnam","visakhapatnam","vizag","Vizag"):
	  	search_char1="Vizag"
	  	search_char2="VIZAG"
	else:
		time.sleep(5)
	  	print "This City Data is not available!!!"
	  	continue				

	url = api_url+'/store/connector/_magic?url=http://startupsclub.org/startupsclubevents/&_apikey='+token
	url=url.replace(' ','%20')
	try:
	    json_obj = urllib2.urlopen(url)
	    data = json.load(json_obj)
	    new_data=data['tables'][0]['results']
	    noofdata=len(new_data)
	    j=0
	    for i in range(noofdata):
	    	name_event=data['tables'][0]['results'][i]['link/_text']
	    	check1=name_event.find(search_char1)
	    	check2=name_event.find(search_char2)
	    	if check1!=-1 or check2!=-1:
	    		j=j+1
	    		dic = {}
		        if 'event_date/_source' in data['tables'][0]['results'][i]:
		        	str_date=data['tables'][0]['results'][i]['event_date/_source']
		        else:
		        	str_date=None
		        if 'econtent_descriptions' in data['tables'][0]['results'][i]:
		        	str_time=data['tables'][0]['results'][i]['econtent_descriptions'][0]
		        else:
		        	str_time=None

		        if 'econtent_descriptions' in data['tables'][0]['results'][i]:
		        	len_descriptions=len(data['tables'][0]['results'][i]['econtent_descriptions'])
		        	if len_descriptions==3:
		        		address=data['tables'][0]['results'][i]['econtent_descriptions'][1]
		        		description=data['tables'][0]['results'][i]['econtent_descriptions'][2]
		       		elif len_descriptions==2:
		       			description=data['tables'][0]['results'][i]['econtent_descriptions'][1]
		       			address="Bangalore"
		       		else:
		       			description=None
		       			address=None	
		       	else:
		       		address=None
		       		description=None



		        dic['str_date'] = str_date
		        dic['str_time']=str_time

		        dic['name']=data['tables'][0]['results'][i]['link/_text']
		        dic['image']=None
		        dic['isReservationRequired']=data['tables'][0]['results'][i]['eventrate_values']
		        
		        address=address.encode('ascii','ignore')
		        description=description.encode('ascii','ignore')
		        dic['locationName']=address
		        dic['description']=description
		        dic['eventLink']=data['tables'][0]['results'][i]['link']
		        dic['name']=dic['name'].encode('ascii','ignore')
		        dic['eventLink']=dic['eventLink'].encode('ascii','ignore')

		        dic['locationName']=dic['locationName'].encode('ascii','ignore')
		        events.append(dic)
	except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
  		print 0  		        
	if j==0:
		print "No Events Available Right now for "+city
	else:
		print "==================== "+str(j)+"======================="
	with open('events_'+city+'_startupsclub.json', 'w') as outfile:
		json.dump(events, outfile,ensure_ascii=False)
	print "==================="+city+"=========================="
	with open('events_'+city+'_startupsclub.json') as data_file:
		d = json.load(data_file)
		pprint(d)          
