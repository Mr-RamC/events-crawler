import urllib2
import json
import httplib
from pprint import pprint

with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['eventBriteApi']['cities']
  token=d['eventBriteApi']['token']
  api_url=d['eventBriteApi']['url']
print cities 
maindic_eventBrite={}
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
        dic['image']="data:image/png;base64,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"
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
      maindic_eventBrite[city]=events
  except httplib.BadStatusLine:
    print 0
  except urllib2.HTTPError:
    print 0
  except urllib2.URLError:
    print 0
  print "==================="+city+" eventBrite =========================="    
with open('events_eventBrite.json', 'w') as outfile:
  json.dump(maindic_eventBrite, outfile,ensure_ascii=False)

