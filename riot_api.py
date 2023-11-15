import requests
import constants
import json

url = 'https://americas.api.riotgames.com/'

def makeAccountRequest(gameName, tagLine):
    query = f'riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={constants.RIOTAPI}'
    return requests.get(url + query)

def makeLeagueRequest(division, tier, queue, page):
    url ='https://na1.api.riotgames.com/'
    query = f'lol/league/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={constants.RIOTAPI}'
    return requests.get(url + query)

def getChampionMasteryInfo(SID):
    url ='https://na1.api.riotgames.com/'
    query = f'lol/champion-mastery/v4/champion-masteries/by-summoner/{SID}?api_key={constants.RIOTAPI}'
    
    return requests.get(url + query)

def parseThroughPage(page, queries):
    playerList = makeLeagueRequest('III', 'SILVER', 'RANKED_SOLO_5x5',page)
    d = {}
    keep = ['championPoints','championId']

    for i in range(queries):
        print(i)
        SID = playerList.json()[i]['summonerId']
        mast = getChampionMasteryInfo(SID)
    
        if mast.status_code == 200:
            mast = mast.json()[:25]
            d[SID] = []
            for entry in mast:
                cleaned = {key: entry[key] for key in keep}
                d[SID].append(cleaned)
        else:
            print(mast.reason)
    
    return d

def saveToJSON(d, filename):
    with open(filename, 'w') as f:
        json.dump(d, f, indent=4)

def updateJSON(d, filename):
    with open(filename, 'r+') as f:
        load = json.load(f)
        print(len(load))
        load.update(d)
        print(len(load))
        f.seek(0)
        json.dump(load, f, indent=4)

d = parseThroughPage(1, 95)
updateJSON(d, 'data/mastery_data.json')








