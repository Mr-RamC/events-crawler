import urllib2
import json
import httplib
from pprint import pprint

events=[]
address=raw_input("Enter City:")
url1 = 'https://www.eventbriteapi.com/v3/events/search/?token=RAD7HQSNEWM7KHTCGXBJ&venue.city='+address+'&sort_by=date'
try:
  json_obj = urllib2.urlopen(url1)
  data = json.load(json_obj)
  noofdata=data['pagination']['object_count']
  for i in range(noofdata):
    dic = {}
    str_date=data['events'][i]['start']['local']
    end_date=data['events'][i]['end']['local']
    dic['date'] = str_date[:10]
    start_time=str_date[11:]
    end_time=end_date[11:]
    time=str(start_time)+"--"+str(end_time)
    dic['time']=time
    dic['name']=data['events'][i]['name']['text']
    venue_id=data['events'][i]['venue_id']
    venue_online=data['events'][i]['online_event']
    if venue_online==False:
      try:
        url2='https://www.eventbriteapi.com/v3/venues/'+venue_id+'/?token=RAD7HQSNEWM7KHTCGXBJ'
        json_obj2 = urllib2.urlopen(url2)
        data2 = json.load(json_obj2)
        address_1=data2['address']['address_1']
        address_2=data2['address']['address_2']
        region=data2['address']['region']
        postal_code=data2['address']['postal_code']
        if address_1 :
          if address_2:
            dic['locationName']=str(address_1)+" "+str(address_2)+" "+str(region)+" "+str(postal_code)
          else:
            dic['locationName']=str(address_1)+" "+str(region)+" "+str(postal_code)
        else:
          dic['locationName']=str(region)+" "+str(postal_code)
                  

      except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
        raise
    else:
      dic['locationName']="Online"
    dic['eventLink']=data['events'][i]['url']
    dic['date']=dic['date'].encode('ascii','ignore')
    dic['time']=dic['time'].encode('ascii','ignore')
    dic['name']=dic['name'].encode('ascii','ignore')
    dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
    events.append(dic)
  with open('2.json', 'w') as outfile:
    json.dump(events, outfile,ensure_ascii=False)

  with open('2.json') as data_file:    
    d = json.load(data_file)
  pprint(d)  
except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
  print 0
