import urllib2
import json
import httplib
from pprint import pprint
import datetime


cities=[]
with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['meetupApi']['cities']
  token=d['meetupApi']['token']
  api_url=d['meetupApi']['url']
print cities  
maindic_meetup={}
for city in cities:
  events=[]
  url = api_url+'/open_events?city='+city+'&country=in&time=,2w&key='+token+'&text_format=plain&page=200&offset=0'
  try:
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    noofdata=data['meta']['count']
    print "======================"
    print noofdata
    print "======================"
    for i in range(noofdata):
      dic = {}
      utc_offset=data['results'][i]['utc_offset']
      utc_offset=utc_offset/1000
      str_date=data['results'][i]['time']
      str_date=datetime.datetime.fromtimestamp(str_date/1000.0)
      str_date=str_date+datetime.timedelta(seconds=utc_offset)-datetime.timedelta(seconds=19800)

      if 'duration' in data['results'][i]:
        duration=data['results'][i]['duration']
        duration=duration/1000
        end_date=str_date+datetime.timedelta(seconds=duration)
      else:
        end_date=None  

      no_people=data['results'][i]['yes_rsvp_count']
      if no_people<10:
        continue
      if 'description' in data['results'][i]:
        description=data['results'][i]['description']
        description=description.encode('ascii','ignore')
        if len(description)<1000:
          dic['description']="No of People Coming: "+str(no_people)+" "+description
        else:
          dic['description']="No of People Coming: "+str(no_people)+" "+description[0:1000]
      else:
        description=None    
        dic['description']=None
      str_date=str_date.strftime ("%Y-%m-%d %H:%M:%S")
      if end_date==None:
        dic['end_date'] =None
        dic['end_time']=None

      else:
        end_date=end_date.strftime ("%Y-%m-%d %H:%M:%S")
        dic['end_date'] = end_date[:10]
        end_time=end_date[11:]
        dic['end_time']=end_time
      dic['str_date'] = str_date[:10]
      str_time=str_date[11:]
      dic['str_time']=str_time

      dic['name']=data['results'][i]['name']
      if 'photo_url' in data['results'][i]:
        dic['image']=data['results'][i]['photo_url']
      else:
        dic['image']="http://img1.meetupstatic.com/img/94156887029318281691566697/logo.svg"
      if description!=None:
        if description.find("registration")==-1:
          dic['isReservationRequired']=False
        else:
          dic['isReservationRequired']=True
      else:
        dic['isReservationRequired']="Unknown"
            
      if 'venue' in data['results'][i]:
        address_1=data['results'][i]['venue']['address_1']
        add_name=data['results'][i]['venue']['name']
      else:
        address_1=None
        add_name=None  
      address=""
      if address_1:
        address_1=address_1.encode('ascii','ignore')
        address+=str(address_1)
      else:
        address+=""  
      if add_name:
        add_name=add_name.encode('ascii','ignore')
        address+=" "+str(add_name)
      else:
        address+=""

      address=address+city
      address=address.encode('ascii','ignore')
      dic['locationName']=address
      dic['eventLink']=data['results'][i]['event_url']
      dic['str_date']=dic['str_date'].encode('ascii','ignore')
      dic['str_time']=dic['str_time'].encode('ascii','ignore')
      dic['name']=dic['name'].encode('ascii','ignore')
      dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
      dic['locationName']=dic['locationName'].encode('ascii','ignore')
      events.append(dic)
      maindic_meetup[city]=events
  except httplib.BadStatusLine:
    print 0
  except urllib2.HTTPError:
    print 0
  except urllib2.URLError:
    print 0
  print "==================="+city+" meetup =========================="  
with open('events_meetup.json', 'w') as outfile:
  json.dump(maindic_meetup, outfile,ensure_ascii=False)
