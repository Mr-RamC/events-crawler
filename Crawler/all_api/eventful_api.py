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
            dic['image']="data:image/png;base64,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"
        else:
          dic['image']="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHsAAAB7CAMAAABjGQ9NAAAAolBMVEX8/vz///8AZMwAYcsEZswAX8sAXcpFqhTp9eOm1pPt9vz5/f0xogAAW8rW6sg3pgDG3PSNsuXS4vSpyupTsSt5wFyt1Zri8Px/qeDB4Layz+8sfdJShda/1e5etTs7dtHg8djv+OuYveglcM8AU8ifw+m33aL2+/NEh9Zfkdp1puEjd9PI5L+53axjmtw/ftWTy3h+wGhouEmbzoXM57eFx2hiv8uJAAAFLUlEQVRoge1XbXuqOBAlb2BJEQi0WCy+gFaEit16/f9/bWcSsVq5z73d7f2ym/O0GpIxJzM5mQmOY2FhYWFhYWFhYWFhYWFhYWFhYWFhYfF/A3E2mw0hwyND3f+Ozfc/2mT8eDgcdstbFrJ5fBt/N3dSzfPz/Acv9DwvfFjemG0ew9Abf6/n2V6INjs9PCIzcIeLzyRkeQy9+5fv5VZzSrky7eUDcIfpbMBvMnrwvPu7P8AdneafgdNvi9HiNuTAHf5R7nEK3E+EDOh80G+i/05tctV/7rzpvpjdcBPDDdTpWI9dLEA3yfKWO8vLuCyU1O31uj8uJCoL3SezBAzyk5iI0t1+XpaJ6fJz5M6zDEQ+2iH3C0acjF52/XFevDxtBrizeM9c4bJpCTP5TbCK+4F2VRXo1aSF8YC2a7O66apay7xmQSCm2KWmnHLOq6qORm8phtxL04cxMN2Hd2a5i9m9t7uJOVHPgiEoE51yVMXY3HgjS5e6E+JErcBBSkUwgRGSMyq6snIZ5VSw0pHxCqlxvPnhmQMGFAfyGnrh+0gz7aB5XH7m9muXM97uK0qp2/jZlFFq0kTWAV9JVA1fFAxggE2kQxLBaYvroYxzUWVOIqDBORM8XszC0Bzu8I48QXOmDzmBMx8+jD7FXJYwE51EWd7Br3kiO8ZFI42AGG2VP6Gc0VhlxRYbIOZEO1x1ZbwHf1cl8dddBdxdmfvO690RuY+H3eiX3GoPsWpAuQTc5O5W5vC8z/SqgKKTqoWvCZpnW8aDjhhu2HGyKWDMhR5icguKmhidv6Kub7mvz3cCXlc6IxHdzLI9bC4qzIeQ81KWnLKpMVgzziqfJBBhDD6YwGrEVl7ltZ4bWtfc3mduGQvKtr4RHbJGTiN4EMMwqm6qCESDmj0gCgUVITccKP3zWHD27H/KLT/hNn5fxFx2LqfbJEesYfuCnOSUiymQrQPceDkFpi43BsDtFsB9DtVPuZ+cX3P7W8FPqNArmNrX7hNnG3CaOH7L+AcojqDfVdZzi3/st+aGJKHhiqCG1DRxMegZhBw057eXBoFb6/1m7de5vSFuWk96rDGUBSgd9I4hJ4b7wiDTZ4xNv8bt3Bnu5fV+w441vnSklESaOuJDMqmiBkRYEEfWsLjYlwa6IKDfX+U+DGkthonqvnhAkcD+MuC8mYLKfVwcaq03iMroN7l7rXm4CmdzHMotORzf068cyJ44J4ngDKHyJtgJ4mb707SqDaaSXMf8Q+fFZ52/4gVmR041/cZvSFaQzYzjUS2E1q8WAWhZM6opnDmdAWQE9cPklgG/uYDkCpt34Te2wveFs1m8h0PcTo4FqstVVLZQtjqdRdZ48MRWzw+JjdOgK5SKQXarZlBrkAxhrZPuGTLt2W9nqSlnh7fU3FtvuGW3woI0n8NH0JrgqgqKBIuliUy3godqDpWFB5hTLrhLZrh1pCjU+Doji95vo26saaDxdIgbbgsMCzj8u/vitJ5mRd1K9QZbPQwGwbPScoA8YNSXuCzodAPqPyDY+nBXDMOZfgEgy790RQ29u3EaYv3evIVGAWfPi25fVdW8LrOzCmo+X39Y5M3cGPj6DDbVPjktq6vmZr1rnGK/VfDS8zKbPW6M7paH9zSdHZ/gfSGd/UAJvKfH6/urr6KiUJn86MlOt7drg/7pYxDsTi1VgAWujWzG4/6WRpzR+HWBL0dL6MSexfj26vyduLrp9nfV84X1j1JbWFhYWFhYWFhYWFhYWFhYWFhYWFj8N/A3pFt9Y3+96bwAAAAASUVORK5CYII="      
      else:
        dic['image']="data:image/png;base64,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"

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
              dic['image']="data:image/png;base64,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"
          else:
            dic['image']="data:image/png;base64,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"      
        else:
          dic['image']="data:image/png;base64,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"

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
  except httplib.BadStatusLine:
    print 0
  except urllib2.HTTPError:
    print 0
  except urllib2.URLError:
    print 0
