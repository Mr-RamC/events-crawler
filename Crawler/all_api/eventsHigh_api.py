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
maindic_eventsHigh={}
for city in cities:
	events=[]

	if city in ("Bangalore","bangalore","Bengaluru","bengaluru"):
	  	search_char="bangalore"
	elif city in ("mumbai","Mumbai"):
	  	search_char="mumbai"
	elif city in ("Chennai","chennai"):
	  	search_char="chennai"
	elif city in ("Delhi","delhi"):
		search_char="delhi"
	else:
		time.sleep(5)
	  	print "This City Data is not available!!!"
	  	continue				

	url = api_url+'/store/connector/_magic?url=https://www.eventshigh.com/'+search_char+'/featured&_apikey='+token
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
	        if '-' in date[1]:
	        	flag=1
	        	new_date=date[1].split("-")
	        	start_date=new_date[0]
	        	start_time=date[2]
	        	end_date=new_date[1]
	        else:
	        	flag=0
	        	start_date=date[1]
	        	start_time=date[2]
	        	end_date=None	
	        if 'action_link/_text' in data['tables'][0]['results'][i]:
	        	descriptions=data['tables'][0]['results'][i]['action_link/_text']
	        	if descriptions=="Book Tickets":
	        		link=data['tables'][0]['results'][i]['action_link']
	        		link=link.encode('ascii','ignore')
	        		dic['isReservationRequired']=True
	        		description="To book tickets and more details go to "+link
	        		description=description.decode('utf-8')
	       		else:
	       			link=data['tables'][0]['results'][i]['action_link']
	       			link=link.encode('ascii','ignore')
	       			description="To book tickets and more details go to "+link
	       			description=description.decode('utf-8')
	       			dic['isReservationRequired']=False
	       	else:
	       		dic['isReservationRequired']="Unknown"
	       		description=None
	       	if date:
	       		if start_date:
	       			try:
	       				start_date=datetime.datetime.strptime(start_date," %d %B %Y ")
	       			except ValueError:
	       				start_date=datetime.datetime.strptime(start_date," %d %b %Y ")	
		        if start_time:
		        	start_time=datetime.datetime.strptime(start_time, " %I:%M%p")
		        if end_date:
		        	try:
		        		end_date=datetime.datetime.strptime(end_date," %d %B %Y ")
		        	except ValueError:
		        		end_date=datetime.datetime.strptime(end_date," %d %b %Y ")	
	       		dic['str_date'] = str(start_date)[:10]
	       		dic['str_time']=str(start_time)[11:]
	       		dic['end_date']=str(end_date)[:10]
	       	else:
	       		dic['str_date']=None
	       		dic['str_time']=None
	       	if 'action_link/_title' in data['tables'][0]['results'][i]:
	       		dic['name']=data['tables'][0]['results'][i]['action_link/_title']
	       		dic['name']=dic['name'].encode('ascii','ignore')
	       	else:
	       		dic['name']=None	
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
	        dic['locationName']=address
#	       	r = urllib2.urlopen(link).read()
#	        soup = BeautifulSoup(r,'html.parser')
#	        img = soup.find("div", class_="details-non-blur-image-container no-crop")
#	        image_link=img.a["href"]

	        image_link="https://www.eventshigh.com/assets/images/logor.png"
	        dic['image']=image_link
	        dic['description']=description
	        dic['eventLink']=link
	        dic['locationName']=dic['locationName'].encode('ascii','ignore')
	        events.append(dic)
	        maindic_eventsHigh[city]=events
	except httplib.BadStatusLine:
		print 0
	except urllib2.HTTPError:
		print 0
	except urllib2.URLError:
		print 0
	if j==0:
		print "No Events Available Right now for "+city
	else:
		print "==================== "+str(j)+"======================="
	print "==================="+city+" eventshigh =========================="	
with open('events_eventsHigh.json', 'w') as outfile:
	json.dump(maindic_eventsHigh, outfile,ensure_ascii=False)     
