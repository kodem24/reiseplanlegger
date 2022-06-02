

addr = 'https://api.entur.io/journey-planner/v3/graphql'

query = """
{
  stopPlace(
    id: "NSR:StopPlace:6298"
  ) {
    id
    name
    estimatedCalls(
      timeRange: 72100,
      numberOfDepartures: 5
    ) {
      realtime
      aimedArrivalTime
      aimedDepartureTime
      expectedArrivalTime
      expectedDepartureTime
      actualArrivalTime
      actualDepartureTime
      date
      forBoarding
      forAlighting
      destinationDisplay {
        frontText
      }
      quay {
        id
        publicCode
      }
      serviceJourney {
        journeyPattern {
          line {
            id
            publicCode
            name
            transportMode
          }
        }
      }
    }
  }
}

"""

import requests
import datetime 

r = requests.post(addr, json = {"query": query})

res = r.json()
print ("de neste 5 turene fra Vettakollen")
print ("linje     destinasjon          avreise      platform" )
print ("-----     -----------          -------      --------" )


trains = res["data"] ["stopPlace"] ["estimatedCalls"] 

for t in trains : 
    linje = t ["serviceJourney"] ["journeyPattern"] ["line"] ["publicCode"]
    dest = t ["destinationDisplay"] ["frontText"] 
    dep = t ["expectedDepartureTime"] 
    plat = t ["quay"] ["publicCode"]
    dt = datetime.datetime.fromisoformat(dep)
    dd = dt.strftime("%H:%M")
    print (f"{linje:9} {dest:20} {dd:10}   {plat}")




