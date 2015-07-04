from django.http import HttpResponse
import json, urllib
from EventAggregator.fetcher import getMeetupEvent, getBriteEvents

DEFAULT_MAX_RESULT = 8

API_INPUT_PARAMS = [
                    "city",
                    "category",
                    "lat",
                    "lon",
                    "pin",
                    "max_results"
                    ] 
#have a common mapping for both meetup and eventbrite
meetupCategoriesDict = {
                  "spirituality":22,
                  "music" : 21,
                  "literature": 18,
                  "sports": 11,
                  "dancing" : 5,
                  "business": 2
                  }
#TODO : use enum for cities and categories

briteCategoriesDict = {
                       "music" : 103,
                       "business": 101,
                       "food": 110,
                       "sports": 108,
                       "spirituality": 114
                       }


#TODO: look for  library support for this
"""splits string based on '&' and generates key val pairs""" 
def parseInputParams(inputParams):
    if inputParams == "" or inputParams is None:
        return None
    sections = inputParams.strip().split('&')
    ret = {}
    for section in sections:
        if '=' not in section:
            continue
        key, val = section.split('=')
        if key == "max_results":
            try:
                ret[key] = int(val)
            except:
                ret[key] = DEFAULT_MAX_RESULT
        else:
            ret[key] = val
    return ret

def inputInvalid(urlFields):
    if urlFields is None: return None
    for key in urlFields:
        if key not in API_INPUT_PARAMS:
            print key
            return True
    
def mapToMeetupFields(urlFields):
    meetupFields = {}
    
    for key in urlFields:
        if key in ['city', 'lat', 'lon']:
            meetupFields[key] = urlFields[key]
        elif key == 'category':
            try:
                meetupFields[key] = meetupCategoriesDict[urlFields['category']]
            except KeyError:
                return None #category unsupported
            
    return meetupFields

def fetchMeetupEvents(urlFieldsParsed, maxResults):
    meetupFields = mapToMeetupFields(urlFieldsParsed)
    if meetupFields is None:
        #return HttpResponse("Invalid API params. category not found")
        return None
    return getMeetupEvent(meetupFields)[:maxResults]

def aggregateResponses(meetup, brite):
    if brite is None:   brite = []
    if meetup is None:  meetup = []
    result = {
      "status": "success",
       "result": meetup + brite}
    return json.dumps(result)

def mapToBriteFields(urlFields):    
    briteFields = {}
    for key in urlFields:
        if key in ['lat', 'lon']:
            briteFields[key] = urlFields[key]
        if key == 'city':
            briteFields['venue.city'] = urlFields[key]
        elif key == 'category':
            try:
                briteFields['categories'] = briteCategoriesDict[urlFields[key]]
            except KeyError:
                print "categories key error"
                return None
        
    briteFields['venue.country'] = 'IN'
    return briteFields

def fetchBriteEvents(urlFields, maxResults):
    briteFields = mapToBriteFields(urlFields)
    if briteFields is None:
        return None
    briteEvents = getBriteEvents(briteFields)
    return briteEvents[:maxResults] if briteEvents is not None else None

def MyErrorResponse(errorMessage):
    result = {
              "status": "failure",
               "result": errorMessage}
    return HttpResponse(json.dumps(result)) #convert this to json response

def getEvents(request, inputParams):
    if inputParams is None or inputParams == "":
        return MyErrorResponse("Invalid input. No params found")
    urlDecoded = urllib.unquote(inputParams).decode('utf8') 
    urlFieldsParsed = parseInputParams(urlDecoded)
    if inputInvalid(urlFieldsParsed):
        return MyErrorResponse("Invalid API params. Allowed params are city, lat, lon and category")
    try:
        maxResults = urlFieldsParsed['max_results']
    except KeyError:
        maxResults = DEFAULT_MAX_RESULT
    print urlFieldsParsed
    
    meetupEvents = fetchMeetupEvents(urlFieldsParsed,  maxResults = int(maxResults/2))
    briteEvents = fetchBriteEvents(urlFieldsParsed, maxResults = maxResults - int(maxResults/2) )
    response = aggregateResponses(meetupEvents, briteEvents)
    print "after aggregateResponses" 
    return HttpResponse(response, content_type = 'application/json')
