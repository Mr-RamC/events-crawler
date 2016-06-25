
import urllib2
import json
import httplib
from pprint import pprint
import datetime
import time
import os


cities=[]
with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['Graph_Api']['cities']
  token=d['Graph_Api']['token']
  api_url=d['Graph_Api']['url']
  def_img=d['Graph_Api']['image']
print cities  
maindic_Graph={}
for city in cities:
	try:
	    events=[]
	    j=0
	    for offset in range(20):
	      url = api_url+'/search?access_token='+token+'&pretty=0&q='+city+'&type=event&limit=100&offset='+str(offset)
	      json_obj = urllib2.urlopen(url)
	      data = json.load(json_obj)
	      noofdata=len(data['data'])
	      for i in range(noofdata):
	        dic = {}

	        if 'description' in data['data'][i]:
	          description=data['data'][i]['description']
	          description=description.encode('ascii','ignore')
	          if len(description)<1000:
	            dic['description']=description
	          else:
	            dic['description']=description[0:1000]
	        else:
	          description=None    
	          dic['description']=None

	        if 'start_time' in data['data'][i]:
	        	str_date=data['data'][i]['start_time']
	        	start_date=str_date.split("T")
	        else:
	          start_date=None
	          dic['str_date']=None
	          dic['str_time']=None
	        if 'end_time' in data['data'][i]:
	        	end_date=data['data'][i]['end_time']
	        	stop_date=end_date.split("T")
	        else:
	          stop_date=None
	          dic['end_date']=None
	          dic['end_time']=None
	        if start_date:
	        	dic['str_date'] = start_date[0]
	        	dic['str_time'] = start_date[1][:8]
	        if stop_date:
	        	dic['stop_date']=stop_date[0]
	        	dic['stop_time']=stop_date[1][:8]

	        dic['name']=data['data'][i]['name']
	        if description!=None:
	          des_lower=description.lower()
	          if des_lower.find("registration")==-1:
	            dic['isReservationRequired']=False
	          else:
	            dic['isReservationRequired']=True
	        else:
	          dic['isReservationRequired']="Unknown"
	        if 'place' in data['data'][i]:
	          if 'name' in data['data'][i]['place']:
	            address=data['data'][i]['place']['name']+" "+city
	            address=address.encode('ascii','ignore')
	          else:
	            address=None
	        else:
	          address=None    
	        dic['locationName']=address
	        dic['image']=def_img

	        dic['eventLink']="https://www.facebook.com/events/"+data['data'][i]['id']
	        dic['str_date']=dic['str_date'].encode('ascii','ignore')
	        dic['str_time']=dic['str_time'].encode('ascii','ignore')
	        dic['name']=dic['name'].encode('ascii','ignore')
	        dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
	        date_object = datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
	        time_now=datetime.datetime.now()
	        time_compare=time_now+datetime.timedelta(days=10)
	        if time_compare>date_object and date_object>=time_now:
	          j=j+1
	          events.append(dic)
	          maindic_Graph[city]=events
	except httplib.BadStatusLine:
		print 0
	except urllib2.HTTPError:
		print 0
	except urllib2.URLError:
		print 0
	print "=================================="+str(j)+"=========================="
	time.sleep(5)    
os.chdir('C:\Users\sk972\Crawler\events_list')	
with open('events_Graph.json', 'w') as outfile:
  json.dump(events, outfile,ensure_ascii=False)
os.chdir('C:\Users\sk972\Crawler\scripts')  
