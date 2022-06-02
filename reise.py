
# stasjonsliste
# Vettakollen
# Majorstua
# Smestad
# Vestli
# Ryen



stasjoner = [
  {"stasjon": "Vettakollen", "id": 6298},
  {"stasjon": "Majorstuen", "id": 58381},
  {"stasjon": "Smestad", "id": 58273},
  {"stasjon": "Grorud", "id": 58216},
  {"stasjon": "Helsfyr", "id": 59516},
]

print()
print ("Reiseplanlegger")
print()

i = 1
gyldig = []
for s in stasjoner:
  snavn = s["stasjon"]
  print (f"  {i}. {snavn}")
  gyldig.append(str(i))
  i = i + 1

print ()
valg = input ("Velg en stasjon: ")

print()

if valg not in gyldig: 
  print (f"Du må velge et tall mellom 1 og {i-1}")
  import sys
  sys.exit()


stasjon = stasjoner [int(valg) - 1] ["id"]
navn = stasjoner [int(valg) - 1] ["stasjon"]
antall = 10


addr = 'https://api.entur.io/journey-planner/v3/graphql'
#stasjon = 58381
#stasjon = 6298 
query = """
{
  stopPlace(
    id: "NSR:StopPlace:"""+ str(stasjon) +""""
  ) {
    id
    name
    estimatedCalls(
      timeRange: 72100,
      numberOfDepartures: """ +str (antall) +""",
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
print (f"De neste {antall} turene fra {navn}")
print ()
print ("Linje     Destinasjon               Avreise      Platform" )
print ("-----     -----------               -------      --------" )


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
    nt = datetime.datetime.now(datetime.timezone.utc)
    dt = datetime.datetime.fromisoformat(dep)
    delta = int((dt - nt).seconds/60)
    if delta <= 15 : 
      dd = f"{delta} min"
      if delta == 0 : 
        dd = "nå"
    else : 
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
    print (f"{linje} {dest:25} {dd:10}   {plat}")
 




