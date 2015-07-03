import requests
import logging
import simplejson as json
from datetime import datetime

eventBriteOauthToken = "SD2PBVBDCZUJJN2RXLID"
eventBriteBaseUrl = "https://www.eventbriteapi.com/v3/events/search?"

meetupAPIKey = "2e472679216b36f533e755c3a5b1e"
meetupBaseEventUrl = "https://api.meetup.com/2/open_events"
    
#TODO: make requests async for better performance
#use grequests https://github.com/kennethreitz/grequests
#TODO: find param to limit number of results of api call and support for pagination
def filterMeetupResults(response):
    response = json.loads(response)
    events = response['results']
    if len(events) == 0:
        return None
    
    results = []
    #print events[0]
    for event in events:
        result = {}#use a fixed object istead of a dictionary
        for key in event:
            #if key in ['start', 'end' ]:
            #   result['resource_uri'] = event[key] #time for both apis??
            if key == 'event_url':
                result['resource_uri'] = event[key]
            elif key == 'name':
                result['name'] = event[key]
            #ERROR convert time to a common format for both event types
            elif key == 'time':
                result['start'] = event[key] + event['utc_offset'] #storing local time
            elif key == 'duration':
                result['end'] = event['time'] + event['duration'] 
            elif key == 'description':
                result['description'] = event[key]
            elif key == 'organizer_id':
                result['organizer_id'] = event[key] #need to fetch organizer details
        result['info_source'] = 'meetup.com'
        results.append(result)
            
    return results

def getOpenEventsNearby(urlParam={}):
    r = requests.get(meetupBaseEventUrl, params = urlParam)    
    print(r.url)    
    return filterMeetupResults(r.text) #responseString  
    #return r.text

def getMeetupEvent(urlParam = {}):
    urlParam['key'] = meetupAPIKey
    urlParam['text_format'] = 'plain'
    urlParam['country'] = 'IN'
    #TODO add something to limit number of responses
    return getOpenEventsNearby(urlParam)

def filterBriterResults(response):
    response = json.loads(response)
    if response['pagination']['object_count'] == 0:
        print "no brite results found"
        return None
    events = response['events']
    results = []
    #print events[0]
    for event in events:
        result = {}#use a fixed object istead of a dictionary
        for key in event:
            try:
                if key in ['url', 'start', 'end' ]:
                    result[key] = event[key] #time for both apis??
                elif key == 'name':
                    result['name'] = event[key]['text']
                elif key == 'description':
                    result['description'] = event[key]['text']
                elif key == 'organizer_id':
                    result['organizer_id'] = event[key] #need to fetch organizer details
            except: 
                print "ERROR! some exception occured as field was NULL"
        result['info_source'] = 'eventbrite.com'
        results.append(result)
            
    return results

def getBriteEvents(urlParam = {}):
    print "in get brite events"
    response = requests.get(
        eventBriteBaseUrl,
        params = urlParam,
        headers = {
            "Authorization": "Bearer " + eventBriteOauthToken,
        },
        #verify = True,  # Verify SSL certificate
    )
    print response.url
    return filterBriterResults(response.text)

