import urllib2
import json
import httplib
from pprint import pprint
import datetime
import time
from bs4 import BeautifulSoup
# for delhi put city name new delhi
cities=[]
with open('details.json') as basic_details:    
	d = json.load(basic_details)
	cities=d['allevents']['cities']
	token=d['allevents']['token']
	api_url=d['allevents']['url']
print cities 
maindic_allevents={}
for city in cities:
	events=[]
	j=0
	categories=["business","concerts","festivals","music","sports","parties","exhibitions","meetups","performance"]
	for category in categories:			
		url = api_url+'/store/connector/_magic?url=https://allevents.in/'+city+'/'+category+'&_apikey='+token
		url=url.replace(' ','%20')
		try:
		    json_obj = urllib2.urlopen(url)
		    data = json.load(json_obj)
		    new_data=data['tables'][0]['results']
		    noofdata=len(new_data)
		    if 'left_link' in data['tables'][0]['results'][0]:
		    	check_ok=1
		    else:
		    	continue

		    for i in range(noofdata):
	    		j=j+1
	    		dic = {}
		        if 'left_link' in data['tables'][0]['results'][i]:
		        	link=data['tables'][0]['results'][i]['left_link']
		        else:
		        	link=None	

		        dic['name']=data['tables'][0]['results'][i]['left_link/_text']
		        if 'left_value' in data['tables'][0]['results'][i]:
		        	address=data['tables'][0]['results'][i]['left_value']+" "+city
		        else:
		        	address="Unknown"
		        dic['category']=category
		        address=address.encode('ascii','ignore')
		  
		        dic['locationName']=address
		        link=link.encode("ascii",'ignore')
		   
		        r = urllib2.urlopen(link).read()
		        soup = BeautifulSoup(r,'html.parser')
		        des_soup = soup.find("p", property="schema:description")
		        str_date_soup= soup.find("span", property="schema:startDate")
		        end_date_soup=soup.find("span", property="schema:endDate")
		        if des_soup:
		        	description=des_soup.text
		        	description=description.replace("\t","")
		        	description=description.replace("\n","")
		        	description=description.encode('ascii','ignore')
		       	else:
		       		description=None	 	
		        if str_date_soup:
		        	str_date=str_date_soup.text
		        	str_date=str_date.replace("\t","")
		        	str_date=str_date.replace("\n","")
		        	str_dates=str_date.split(" at ")
		        	start_time=str_dates[1]
		        	start_date=str_dates[0]
		        else:
		        	start_time=None
		        	start_date=None	
		        if end_date_soup:
		        	end_date=end_date_soup.text
		        	end_dates=end_date.split(" at ")
		        	stop_time=end_dates[1]
		        	stop_date=end_dates[0]
		        else:
		        	stop_time=None
		        	stop_date=None
		        if 'lazy_image' in data['tables'][0]['results'][i]:
		        	image_link=data['tables'][0]['results'][i]['lazy_image']
		        else:
		        	image_link="http://az771537.vo.msecnd.net/new/images/logonew.png"
		        if start_date:
		       		str_date=datetime.datetime.strptime(start_date,"%a %b %d %Y")
		        if start_time:
		        	str_time=datetime.datetime.strptime(start_time, "%I:%M %p")
		   
		        if stop_date:
		        	stop_date=stop_date.split("to")
		        	stop_date=datetime.datetime.strptime(stop_date[1], " %a %b %d %Y")
		        if stop_time:
		        	stop_time=datetime.datetime.strptime(stop_time, "%H:%M %p")	
		        dic['str_time']=str(str_time)
		        dic['str_date']=str(str_date)
		        dic['stop_date']=str(stop_date)
		        dic['stop_time']=str(stop_time)
		        dic['image']=image_link
		        dic['description']=description
		        dic['eventLink']=link
		        dic['name']=dic['name'].encode('ascii','ignore')
		        dic['eventLink']=dic['eventLink'].encode('ascii','ignore')

		        dic['locationName']=dic['locationName'].encode('ascii','ignore')
		        date_object = datetime.datetime.strptime(start_date, '%a %b %d %Y')
		        time_now=datetime.datetime.now()
		        time_compare=time_now+datetime.timedelta(days=10)
		        if time_compare<date_object:
		        	break
		        if j==50:
		        	break	
		        events.append(dic)
		        maindic_allevents[city]=events
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
	print "==================="+city+" allevents =========================="	
with open('events__allevents.json', 'w') as outfile:
	json.dump(maindic_allevents, outfile,ensure_ascii=False)
