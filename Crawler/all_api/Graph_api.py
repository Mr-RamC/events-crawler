
import urllib2
import json
import httplib
from pprint import pprint
import datetime
import time


cities=[]
with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['Graph_Api']['cities']
  token=d['Graph_Api']['token']
  api_url=d['Graph_Api']['url']
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
	        dic['image']="data:image/jpeg;base64,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"

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
with open('events_Graph.json', 'w') as outfile:
  json.dump(events, outfile,ensure_ascii=False)
