import pandas as pd
import json
from time import time, sleep
import aiohttp
import asyncio

GAMEDLE_URL         = "https://www.gamedle.wtf/giveItATryWritten" #"https://webhook.site/5239c4ad-1547-4c10-bcb6-87797b1facda"
GAMEDLE_POST_HEADER = {"content-type": "application/json"}
GAMEDLE_POST_BODY   = json.loads("{\"gameStatus\":\"IN_PROGRESS\",\"attemps\":[{\"value\":\"\",\"label\":\"\"}],\"original\":{\"value\":1876,\"label\":null,\"platforms\":[],\"genres\":[],\"collection\":352,\"releaseYear\":null,\"tokens\":null,\"involved_companies\":[],\"game_engines\":[],\"game_modes\":[],\"player_perspectives\":[],\"s3_id\":null,\"s3_artwork_id\":null,\"summary\":null,\"themes\":[],\"franchises\":[554],\"collectionFranchisesCoincidence\":null,\"collectionFranchisesCoincidenceNames\":null,\"ytlink\":null,\"steamlink\":null,\"platformsCoincidence\":0,\"genresCoincidence\":0,\"collectionCoincidence\":false,\"releaseYearCoincidence\":0,\"involved_companiesCoincidence\":0,\"game_enginesCoincidence\":0,\"game_modesCoincidence\":0,\"player_perspectiveCoincidence\":0,\"themesCoincidence\":0},\"originalWritten\":null,\"statistics\":{\"current_streaks\":0,\"played\":0,\"max_streaks\":0,\"current_attemps_number\":0,\"dayid\":null},\"settings\":{\"startYear\":null,\"endYear\":null,\"sportsIncluded\":false,\"indieIncluded\":false,\"racingIncluded\":false,\"shooterIncluded\":false,\"actionShowed\":true,\"adventureShowed\":true,\"extendWritten\":false,\"extendUnlimited\":false,\"level\":0},\"usedClue\":false,\"dayid\":null}")
CPU_COUNT           = 12


async def extractData(target, gameId):
    
    gameData = {
        "value": gameId,
        "platforms": list(map(lambda x: x["id"], target["platforms"])),
        "genres": list(map(lambda x: x["id"], target["genres"])),
        "collection": target["collection"],
        "releaseYear": target["releaseYear"],
        "companies": list(map(lambda x: x["id"], target["involved_companies"])),
        "engines": list(map(lambda x: x["id"], target["game_engines"])),
        "modes": target["game_modes"],
        "perspectives": target["player_perspectives"],
        "themes": list(map(lambda x: x["id"], target["themes"])),
        "franchises": [] if target["franchises"] is None else target["franchises"]
    }
    
    return pd.DataFrame([gameData])

async def scrapeGameData(gameId, gameName, session:aiohttp.ClientSession):
    postBody = GAMEDLE_POST_BODY
    postBody["attemps"][0]["value"] = str(gameId)
    postBody["attemps"][0]["label"] = gameName
    postBodyJson = json.dumps(postBody)
    async with session.post(GAMEDLE_URL, headers=GAMEDLE_POST_HEADER, data=postBodyJson) as rsp:
        print(f"Scraping {gameName}...")
        try:
            responseText = await rsp.text()
            parsedResponse = json.loads(responseText)["attemps"][0]
        except:
            print(gameName)
            print(responseText)
            raise
    gameData = await extractData(parsedResponse, gameId)
    print(f"Finished {gameName}...")
    return gameData


async def main(): 
    start = time()
    print("Loading games from JSON")
    gameList = pd.read_json("gameList.json")
    gameDataList = []

    async with aiohttp.ClientSession() as session:
        for _,id,name in gameList.itertuples():
            gameData = await scrapeGameData(id, name, session)
            gameDataList.append(gameData)
    await session.close()

    gameData = pd.concat(gameDataList)
    gameList = gameList.merge(gameData, left_on="value", right_on="value")

    

    end = time()
    print("Elapsed time:", end - start)
    gameList.to_json("finalList.json", orient="records")



if __name__ == "__main__":
    asyncio.run(main())


