#!/usr/bin/env python

import urllib.request
import urllib.parse
import urllib
import requests
import json
import datetime
import sys
#import dataset - deprecated
import psycopg2


"""
make a call API-NG
"""

def callAping(jsonrpc_req):
    try:
        conn = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=('client-2048.crt', 'client-2048.key'), headers=headers)
        resp_json = conn.json()
        sessionToken=resp_json['sessionToken']
        appKey = '2mFk5Wl2BHvVl5OL'
        header2 = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}
        
        url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), header2)
        response = urllib.request.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse.decode('utf-8')
    except urllib.error.URLError:
        print ('Oops no service available at ' + str(url))
        exit()
    except urllib.error.HTTPError:
        print ('Oops not a valid operation from the service ' + str(url))
        exit()


"""
calling getEventTypes operation
"""

def getEventTypes():
    event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
    eventTypesResponse = callAping(event_type_req)
    eventTypeLoads = json.loads(eventTypesResponse)

    try:
        eventTypeResults = eventTypeLoads['result']
        return eventTypeResults
    except:
        print ('Exception from API-NG' + str(eventTypeLoads['error']))
        exit()


"""
Extraction eventypeId for eventTypeName from evetypeResults
"""

def getEventTypeIDForEventTypeName(eventTypesResult, requestedEventTypeName):
    if(eventTypesResult is not None):
        for event in eventTypesResult:
            eventTypeName = event['eventType']['name']
            if( eventTypeName == requestedEventTypeName):
                return  event['eventType']['id']
    else:
        print ('Oops there is an issue with the input')
        exit()


"""
Calling marketCatalouge to get marketDetails
"""
#var requestFilters = '{"filter":{"eventTypeIds": [' + eventId + '],"marketCountries":["GB"],"marketTypeCodes":["MATCH_ODDS"],"marketStartTime":{"from":"'+jsonDate+'"}},"sort":"FIRST_TO_START","maxResults":"1000","marketProjection":["COMPETITION","EVENT"]}}';

#jsonRequest = constructJsonRpcRequest('listMarketCatalogue', requestFilters );


def getMarketCatalogueForNextGBWin(eventTypeID):
    if (eventTypeID is not None):
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        market_catalogue_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketCountries":["GB"],"marketTypeCodes":["MATCH_ODDS"],'\
'"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"100","marketProjection":["RUNNER_METADATA","COMPETITION","EVENT"]}, "id": 1}'
        market_catalogue_response = callAping(market_catalogue_req)
        print (market_catalogue_response)
        
        market_catalogue_loads = json.loads(market_catalogue_response)

        try:
            market_catalogue_results = market_catalogue_loads['result']
            return market_catalogue_results
        except:
            print  ('Exception from API-NG' + str(market_catalogue_results['error']))
            exit()


def getMarketId(marketCatalogueResult):
    if( marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['marketId']


def getSelectionId(marketCatalogueResult):
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['runners'][0]['selectionId']


def getMarketBookBestOffers(marketId):
    market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'
    market_book_response = callAping(market_book_req)
    market_book_loads = json.loads(market_book_response)
    try:
        market_book_result = market_book_loads['result']
        return market_book_result
    except:
        print  ('Exception from API-NG' + str(market_book_result['error']))
        exit()


def printPriceInfo(market_book_result):
    if(market_book_result is not None):
        print ('Please find Best three available prices for the runners')
        for marketBook in market_book_result:
            runners = marketBook['runners']
            for runner in runners:
                print ('Selection id is ' + str(runner['selectionId']))
                if (runner['status'] == 'ACTIVE'):
                    print ('Available to back price :' + str(runner['ex']['availableToBack']))
                    print ('Available to lay price :' + str(runner['ex']['availableToLay']))
                else:
                    print ('This runner is not active')


def placeFailingBet(marketId, selectionId):
    if( marketId is not None and selectionId is not None):
        print ('Calling placeOrder for marketId :' + marketId + ' with selection id :' + str(selectionId))
        place_order_Req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/placeOrders", "params": {"marketId":"' + marketId + '","instructions":'\
                                                                                                                              '[{"selectionId":"' + str(
            selectionId) + '","handicap":"0","side":"BACK","orderType":"LIMIT","limitOrder":{"size":"0.01","price":"1.50","persistenceType":"LAPSE"}}],"customerRef":"test12121212121"}, "id": 1}'
        place_order_Response = callAping(place_order_Req)
        place_order_load = json.loads(place_order_Response)
        try:
            place_order_result = place_order_load['result']
        except:
            print  ('Exception from API-NG' + str(place_order_result['error']))
def savingdata(value1,value2,value3,value4,value5):

    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print ("I am unable to connect to the database")

    cur=conn.cursor()

    sql='INSERT INTO games (hometeam,awayteam,gamedate,compid,comname) values (%s, %s,%s,%s,%s)'

    cur.execute(sql, (value1, value2,value3,value4,value5))
    conn.commit() 
    cur.close()
    conn.close()

url = "https://api.betfair.com/exchange/betting/json-rpc/v1"

"""
headers = { 'X-Application' : 'xxxxxx', 'X-Authentication' : 'xxxxx' ,'content-type' : 'application/json' }

args = len(sys.argv)

if ( args < 3):
    print ('Please provide Application key and session token')
    appKey = raw_input('Enter your application key :')
    sessionToken = raw_input('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
else:
    appKey = sys.argv[1]
    sessionToken = sys.argv[2]

headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}
"""

payload = 'username=andybenson1964&password=atb100364'
headers = {'X-Application': '2mFk5Wl2BHvVl5OL', 'Content-Type': 'application/x-www-form-urlencoded'}

eventTypesResult = getEventTypes()
horseRacingEventTypeID = getEventTypeIDForEventTypeName(eventTypesResult, 'Soccer')


marketCatalogueResult = getMarketCatalogueForNextGBWin(horseRacingEventTypeID)
#print marketCatalogueResult
valcompold=''
save=False
#marketid = getMarketId(marketCatalogueResult)
#print marketid
#market_book_result = getMarketBookBestOffers(marketid)
#printPriceInfo(market_book_result)

for i in range(0, len(marketCatalogueResult)): 
    marketid=marketCatalogueResult[i]['marketId']
    market_book_result = getMarketBookBestOffers(marketid)
    printPriceInfo(market_book_result)
    tabdata=marketCatalogueResult[i]

    for key, value in tabdata.items():
        if (key=='competition'):
             for keycomp,valcomp in value.items():
              #if (valcomp<>valcompold):
              #   print valcomp
              #   valcompold=valcomp
              #print valcomp
              if (valcomp=='English Premier League'):
                save=True
                valid='E0'
              elif (valcomp=='The Championship'):
                save=True
                valid='E1'
              elif (valcomp=='League One'):
                save=True
                valid='E2'
              elif (valcomp=='League Two'):
                save=True
                valid='E3'
              else:
                save=False 
        if (key=='event' and save==True):
             event = dict(value);
             for key2,value2 in event.items():
                 
                 if (key2=='name'):
                   Pos=value2.index(' v ')
                   HomeTeam=value2[:Pos]
                   print (HomeTeam)
                   AwayTeam=value2[Pos+3:]
                   print (AwayTeam)
                   Teams=value2
                 if (key2=='openDate'):
                   Pos=value2.index('T')
                   GameDate=value2[:Pos]
                   
                   print (GameDate)
        if (save==True):
            # insert into database 
            print ("sd")
            #savingdata(HomeTeam,AwayTeam,GameDate,valid,valcomp); 


#marketid = getMarketId(marketCatalogueResult)
#runnerId = getSelectionId(marketCatalogueResult)
#market_book_result = getMarketBookBestOffers(marketid)
#printPriceInfo(market_book_result)

# placeFailingBet(marketid, runnerId)



