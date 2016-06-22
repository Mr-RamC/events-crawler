import urllib2
import json
import httplib
from pprint import pprint
import datetime

cities=[]
with open('details.json') as basic_details:    
  d = json.load(basic_details)
  cities=d['eventfulApi']['cities']
  token=d['eventfulApi']['token']
  api_url=d['eventfulApi']['url']
print cities  
maindic_eventful={}
for city in cities:
  events=[]
  url = api_url+'/events/search?...&location='+city+'&date=Next week&app_key='+token+'&page_size=100&sort_order=date'
  url=url.replace(' ','%20')

  try:
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    noofdata=data['total_items']
    noofdata=noofdata.encode('ascii','ignore')
    noofdata=int(noofdata)
    print "======================"
    print noofdata
    print "======================"
    if noofdata==0:
      print "No Data Found For : "+city
      continue
    elif noofdata==1:
      dic={}
      if 'start_time' in data['events']['event']:
        str_date=data['events']['event']['start_time']
      else:
        str_date=None
      if 'stop_time' in data['events']['event']:
        end_date=data['events']['event']['stop_time']
      else:
        end_date=None  
      no_people=data['events']['event']['going_count']
      if no_people is None:
        no_ppl="Unknown"
      else:
        no_ppl=no_people  
      if 'description' in data['events']['event']:
        description=data['events']['event']['description']
        if description:
          description=description.encode('ascii','ignore')
          if len(description)<1000:
            dic['description']="No of People Coming: "+str(no_ppl)+" "+description
          else:
            dic['description']="No of People Coming: "+str(no_ppl)+" "+description[0:1000]
        else:
          if no_ppl!="Unknown":
            dic['description']="No of People Coming: "+str(no_ppl)
          else:
            dic['description']=None
      else:
        description=None    
        dic['description']=None

      if str_date==None:
        dic['str_date'] =None
        dic['str_time']=None
      else:
        dic['str_date'] = str_date[:10]
        str_time=str_date[11:]
        dic['str_time']=str_time

      if end_date==None:
        dic['end_date'] =None
        dic['end_time']=None  

      else:
        dic['end_date'] = end_date[:10]
        end_time=end_date[11:]
        dic['end_time']=end_time

      dic['name']=data['events']['event']['title']
      if 'image' in data['events']['event']:
        if data['events']['event']['image']:
          if 'url' in data['events']['event']['image']:
            dic['image']=data['events']['event']['image']['url']
          else:
            dic['image']=None
        else:
          dic['image']=None      
      else:
        dic['image']=None

      dic['isReservationRequired']="Unknown"
      address=""      
      if 'venue_name' in data['events']['event']:
        venue_name=data['events']['event']['venue_name']
        if venue_name==None:
          address+=""
        else:
          address+=venue_name+" " 
      else:
        venue_name=""
        address+=""
      if 'venue_address' in data['events']['event']:
        venue_address=data['events']['event']['venue_address']
        if venue_address==None:
          address+=""
        else:
          address+=venue_address+" "  
      else:
        venue_address=""
        address+=""
      if 'region_name' in data['events']['event']:
        region_name=data['events']['event']['region_name']
        if region_name==None:
          address+=""
        else:
          address+=region_name+" "  
      else:
        region_name=""
        address+=""
      if 'postal_code' in data['events']['event']:
        postal_code=data['events']['event']['postal_code']
        if postal_code==None:
          address+=""
        else:
          address+=postal_code+" "  
      else:
        postal_code=""
        address+=""
      address+=city
      address=address.encode('ascii','ignore')
      dic['locationName']=address
      dic['eventLink']=data['events']['event']['url']
      dic['name']=dic['name'].encode('ascii','ignore')
      dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
      dic['locationName']=dic['locationName'].encode('ascii','ignore')
      events.append(dic)
      maindic_eventful[city]=events
      with open('events_eventful.json', 'w') as outfile:
        json.dump(maindic_eventful, outfile,ensure_ascii=False)

    else:
      for i in range(noofdata):
        dic = {}
        if 'start_time' in data['events']['event'][i]:
          str_date=data['events']['event'][i]['start_time']
        else:
          str_date=None
        if 'stop_time' in data['events']['event'][i]:
          end_date=data['events']['event'][i]['stop_time']
        else:
          end_date=None  
        no_people=data['events']['event'][i]['going_count']
        if no_people is None:
          no_ppl="Unknown"
        else:
          no_ppl=no_people  
        if 'description' in data['events']['event'][i]:
          description=data['events']['event'][i]['description']
          if description:
            description=description.encode('ascii','ignore')
            if len(description)<1000:
              dic['description']="No of People Coming: "+str(no_ppl)+" "+description
            else:
              dic['description']="No of People Coming: "+str(no_ppl)+" "+description[0:1000]
          else:
            if no_ppl!="Unknown":
              dic['description']="No of People Coming: "+str(no_ppl)
            else:
              dic['description']=None
        else:
          description=None    
          dic['description']=None

        if str_date==None:
          dic['str_date'] =None
          dic['str_time']=None
        else:
          dic['str_date'] = str_date[:10]
          str_time=str_date[11:]
          dic['str_time']=str_time

        if end_date==None:
          dic['end_date'] =None
          dic['end_time']=None  

        else:
          dic['end_date'] = end_date[:10]
          end_time=end_date[11:]
          dic['end_time']=end_time

        dic['name']=data['events']['event'][i]['title']
        if 'image' in data['events']['event'][i]:
          if data['events']['event'][i]['image']:
            if 'url' in data['events']['event'][i]['image']:
              dic['image']=data['events']['event'][i]['image']['url']
            else:
              dic['image']=None
          else:
            dic['image']=None      
        else:
          dic['image']=None

        dic['isReservationRequired']="Unknown"
        address=""      
        if 'venue_name' in data['events']['event'][i]:
          venue_name=data['events']['event'][i]['venue_name']
          if venue_name==None:
            address+=""
          else:
            address+=venue_name+" " 
        else:
          venue_name=""
          address+=""
        if 'venue_address' in data['events']['event'][i]:
          venue_address=data['events']['event'][i]['venue_address']
          if venue_address==None:
            address+=""
          else:
            address+=venue_address+" "  
        else:
          venue_address=""
          address+=""
        if 'region_name' in data['events']['event'][i]:
          region_name=data['events']['event'][i]['region_name']
          if region_name==None:
            address+=""
          else:
            address+=region_name+" "  
        else:
          region_name=""
          address+=""
        if 'postal_code' in data['events']['event'][i]:
          postal_code=data['events']['event'][i]['postal_code']
          if postal_code==None:
            address+=""
          else:
            address+=postal_code+" "  
        else:
          postal_code=""
          address+=""
        address+=city
        address=address.encode('ascii','ignore')
        dic['locationName']=address
        dic['eventLink']=data['events']['event'][i]['url']
        dic['name']=dic['name'].encode('ascii','ignore')
        dic['eventLink']=dic['eventLink'].encode('ascii','ignore')
        dic['locationName']=dic['locationName'].encode('ascii','ignore')
        events.append(dic)
        maindic_eventful[city]=events
      with open('events_eventful.json', 'w') as outfile:
        json.dump(maindic_eventful, outfile,ensure_ascii=False)
  except httplib.BadStatusLine and urllib2.URLError and urllib2.HTTPError:
    print 0
