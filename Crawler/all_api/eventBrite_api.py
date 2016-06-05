import urllib2
import json
import httplib
from pprint import pprint


cities=[]
with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['eventBriteApi']['cities']
  token=d['eventBriteApi']['token']
  api_url=d['eventBriteApi']['url']
print cities 

for city in cities:
  events=[]
  url1 = api_url+'/events/search/?token='+token+'&venue.city='+city+'&sort_by=date'
  try:
    json_obj = urllib2.urlopen(url1)
    data = json.load(json_obj)
    noofdata1=data['pagination']['object_count']
    if noofdata1>=50:
      noofdata=50
    else:
      noofdata=noofdata1  
    for i in range(noofdata):
      dic = {}
      str_date=data['events'][i]['start']['local']
      end_date=data['events'][i]['end']['local']
      dic['str_date'] = str_date[:10]
      dic['end_date'] = end_date[:10]
      str_time=str_date[11:]
      end_time=end_date[11:]
      dic['str_time']=str_time
      dic['end_time']=end_time
      dic['name']=data['events'][i]['name']['text']
      venue_id=data['events'][i]['venue_id']
      venue_online=data['events'][i]['online_event']
      logo_id=data['events'][i]['logo_id']
      dic['isReservationRequired']=data['events'][i]['is_reserved_seating']
      if logo_id is None:
        dic['image']=None
      else:
        dic['image']=data['events'][i]['logo']['url']  
      if venue_online==False:
        try:
          url2=api_url+'/venues/'+venue_id+'/?token='+token
          json_obj2 = urllib2.urlopen(url2)
          data2 = json.load(json_obj2)
          address_1=data2['address']['address_1']
          address_2=data2['address']['address_2']
          region=data2['address']['region']
          postal_code=data2['address']['postal_code']
          address=""
          if address_1:
            address+=str(address_1)
          else:
            address+=""
          if address_2:
            address+=" "+str(address_2)
          else:
            address+=""
          if region:
            address+=" "+str(region)
          else:
            address+=""
          if postal_code:
            address+=" "+str(postal_code)
          else:
            address+=""
          if address=="":
            dic['locationName']=None
          else:
            dic['locationName']=address
                  
        except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
          raise
      else:
        dic['locationName']="Online"
      dic['eventLink']=data['events'][i]['url']
      dic['str_date']=dic['str_date'].encode('ascii','ignore')
      dic['str_time']=dic['str_time'].encode('ascii','ignore')
      dic['end_date']=dic['end_date'].encode('ascii','ignore')
      dic['end_time']=dic['end_time'].encode('ascii','ignore')
      dic['name']=dic['name'].encode('ascii','ignore')
      dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
      events.append(dic)
    with open('events_'+city+'_eventBrite.json', 'w') as outfile:
      json.dump(events, outfile,ensure_ascii=False)
    print "==================="+city+"=========================="
    with open('events_'+city+'_eventBrite.json') as data_file:    
      d = json.load(data_file)
    pprint(d)  
  except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
    print 0
