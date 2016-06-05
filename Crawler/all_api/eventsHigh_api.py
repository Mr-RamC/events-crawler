import urllib2
import json
import httplib
from pprint import pprint
import datetime
import time
from bs4 import BeautifulSoup

cities=[]
with open('details.json') as basic_details:    
	d = json.load(basic_details)
	cities=d['eventsHigh']['cities']
	token=d['eventsHigh']['token']
	api_url=d['eventsHigh']['url']
print cities 

for city in cities:
	events=[]

	if city in ("Bangalore","bangalore","Bengaluru","bengaluru"):
	  	search_char="bangalore"
	elif city in ("mumbai","Mumbai"):
	  	search_char="mumbai"
	elif city in ("Chennai","chennai"):
	  	search_char2="chennai"
	elif city in ("Delhi","delhi"):
		search_char="delhi"
	else:
		time.sleep(5)
	  	print "This City Data is not available!!!"
	  	continue				

	url = api_url+'/store/connector/_magic?url=https://www.eventshigh.com/'+search_char+'/featured&_apikey='+token
	url=url.replace(' ','%20')
	try:
	    json_obj = urllib2.urlopen(url)
	    data = json.load(json_obj)
	    new_data=data['tables'][0]['results']
	    noofdata=len(new_data)
	    j=0
	    for i in range(noofdata):
    		j=j+1
    		dic = {}
	        if 'ehnowrap_value' in data['tables'][0]['results'][i]:
	        	str_date=data['tables'][0]['results'][i]['ehnowrap_value']
	        	date=str_date.split(",")
	        else:
	        	str_date=None
	        if 'action_link/_text' in data['tables'][0]['results'][i]:
	        	descriptions=data['tables'][0]['results'][i]['action_link/_text']
	        	if descriptions=="Book Tickets":
	        		link=data['tables'][0]['results'][i]['action_link']
	        		dic['isReservationRequired']=True
	        		description="To book tickets and more details go to "+link
	       		else:
	       			link=data['tables'][0]['results'][i]['action_link']
	       			description="To book tickets and more details go to "+link
	       			dic['isReservationRequired']=False
	       	else:
	       		dic['isReservationRequired']="Unknown"
	       		description=None
	       	if date:
	       		dic['str_date'] = date[1]
	       		dic['str_time']=date[2]
	       	else:
	       		dic['str_date']=None
	       		dic['str_time']=None
	        dic['name']=data['tables'][0]['results'][i]['action_link/_title']
	        if 'capitalize_link/_text' in data['tables'][0]['results'][i]:
	        	address=data['tables'][0]['results'][i]['capitalize_link/_text']+" "+city
	        else:
	        	address="Unknown"
	        categories=[]
	        if 'browseorange_link_1/_text' in data['tables'][0]['results'][i]:
	        	category=data['tables'][0]['results'][i]['browseorange_link_1/_text']
	        	category=category.encode('ascii','ignore')
	        	categories.append(category)
	        if 'browseorange_link_2/_text' in data['tables'][0]['results'][i]:
	        	category=data['tables'][0]['results'][i]['browseorange_link_2/_text']
	        	category=category.encode('ascii','ignore')
	        	categories.append(category)
	        dic['category']=categories
	        address=address.encode('ascii','ignore')
	        description=description.encode('ascii','ignore')
	        dic['locationName']=address
	        r = urllib2.urlopen(link).read()
	        soup = BeautifulSoup(r,'html.parser')
	        img = soup.find("div", class_="details-non-blur-image-container no-crop")
	        image_link=img.a["href"]
	        dic['image']=image_link
	        dic['description']=description
	        dic['eventLink']=link
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
	with open('events_'+city+'_eventsHigh.json', 'w') as outfile:
		json.dump(events, outfile,ensure_ascii=False)
	print "==================="+city+"=========================="
	with open('events_'+city+'_eventsHigh.json') as data_file:
		d = json.load(data_file)
		pprint(d)          
