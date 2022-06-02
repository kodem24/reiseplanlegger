

addr = 'https://api.entur.io/journey-planner/v3/graphql'
#stasjon = 58381
stasjon = 6298 
query = """
{
  stopPlace(
    id: "NSR:StopPlace:"""+ str(stasjon) +""""
  ) {
    id
    name
    estimatedCalls(
      timeRange: 72100,
      numberOfDepartures: 5,
      whiteListedModes: [metro]
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

from xtermcolor import colorize 

l1 = 0x039bd1 
l2 = 0xf15902
l3 = 0xa465a2
l4 = 0x154583
l5 = 0x40a844


for t in trains : 
    linje = t ["serviceJourney"] ["journeyPattern"] ["line"] ["publicCode"]
    dest = t ["destinationDisplay"] ["frontText"] 
    dep = t ["expectedDepartureTime"] 
    plat = t ["quay"] ["publicCode"]
    dt = datetime.datetime.fromisoformat(dep)
    dd = dt.strftime("%H:%M")
    farge = l1 
    if linje == "1" : 
      farge = l1 
    elif linje == "2" :
      farge = l2 
    elif linje == "3" :
      farge = l3
    elif linje == "4" :
      farge = l4
    elif linje == "5" :
      farge = l5
    
    linje = colorize (f"{linje:9}", rgb = farge)
    print (f"{linje} {dest:20} {dd:10}   {plat}")
 




