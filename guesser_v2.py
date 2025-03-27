import pandas as pd
from math import log2

def calculate_entropy(dataframe, gameId):
    #print(f"game id: {gameId}")
    total_entropy = 0
    for year in ["<",">","="]:
        for genre in ["g","r","y"]:
            for theme in ["g","r","y"]:
                newDf = filter(dataframe, gameId, genre, theme, year)
                if len(newDf.index) > 0:
                    p = len(newDf.index) / len(dataframe.index)
                    entropy = log2(p) * (-1) * p
                    # print(f"({gameId}, {genre}, {theme}, {year}): {entropy}")
                    total_entropy += entropy
                # else:
                #     print(f"({gameId}, {genre}, {theme}, {year}): Ignoring...")
    return total_entropy


def filter(dataframe: pd.DataFrame, guessResults):
    guess = dataframe.loc[dataframe["value"] == int(guessResults[0])]
    originalCount = len(dataframe.index)
    guessPlatforms = guess.iat[0,2]
    guessGenres = guess.iat[0,3]
    guessCollection = guess.iat[0,4]
    guessYear = guess.iat[0,5]
    guessCompanies = guess.iat[0,6]
    guessEngines = guess.iat[0,7]
    guessModes = guess.iat[0,8]
    guessPerspectives = guess.iat[0,9]
    guessThemes = guess.iat[0,10]
    guessFranchises = guess.iat[0,11]
    
    if(guessResults[1] == "g"):
        dataframe = dataframe.loc[dataframe["platforms"] == guessPlatforms]
    elif(guessResults[1] == "r"):
        dataframe = dataframe.loc[dataframe["platforms"].apply(lambda x: x.isdisjoint(guessPlatforms))]
    else:
        dataframe = dataframe.loc[dataframe["platforms"].apply(lambda x: not (x.isdisjoint(guessPlatforms) or x == guessPlatforms))]

    if(guessResults[2] == "g"):
        dataframe = dataframe.loc[dataframe["genres"] == guessGenres]
    elif(guessResults[2] == "r"):
        dataframe = dataframe.loc[dataframe["genres"].apply(lambda x: x.isdisjoint(guessGenres))]
    else:
        dataframe = dataframe.loc[dataframe["genres"].apply(lambda x: not (x.isdisjoint(guessGenres) or x == guessGenres))]

    if(guessResults[4] == "="):
        dataframe = dataframe.loc[dataframe["releaseYear"] == guessYear]
    elif(guessResults[4] == ">"):
        dataframe = dataframe.loc[dataframe["releaseYear"] > guessYear]
    else:
        dataframe = dataframe.loc[dataframe["releaseYear"] < guessYear]

    if(guessResults[7] == "g"):
        dataframe = dataframe.loc[dataframe["companies"] == guessCompanies]
    elif(guessResults[7] == "r"):
        dataframe = dataframe.loc[dataframe["companies"].apply(lambda x: x.isdisjoint(guessCompanies))]
    else:
        dataframe = dataframe.loc[dataframe["companies"].apply(lambda x: not (x.isdisjoint(guessCompanies) or x == guessCompanies))]
        
    if(guessResults[6] == "g"):   
        dataframe = dataframe.loc[dataframe["engines"] == guessEngines]
    elif(guessResults[6] == "r"):
        dataframe = dataframe.loc[dataframe["engines"].apply(lambda x: x.isdisjoint(guessEngines))]
    else:
        dataframe = dataframe.loc[dataframe["engines"].apply(lambda x: not (x.isdisjoint(guessEngines) or x == guessEngines))]

    if(guessResults[5] == "g"):
        dataframe = dataframe.loc[dataframe["modes"] == guessModes]
    elif(guessResults[5] == "r"):
        dataframe = dataframe.loc[dataframe["modes"].apply(lambda x: x.isdisjoint(guessModes))]
    else:
        dataframe = dataframe.loc[dataframe["modes"].apply(lambda x: not (x.isdisjoint(guessModes) or x == guessModes))]

    if(guessResults[8] == "g"):
        dataframe = dataframe.loc[dataframe["perspectives"] == guessPerspectives]       
    elif(guessResults[8] == "r"):    
        dataframe = dataframe.loc[dataframe["perspectives"].apply(lambda x: x.isdisjoint(guessPerspectives))]
    else:
        dataframe = dataframe.loc[dataframe["perspectives"].apply(lambda x: not (x.isdisjoint(guessPerspectives) or x == guessPerspectives))]

    if(guessResults[3] == "g"):
        dataframe = dataframe.loc[dataframe["themes"] == guessThemes]
    elif(guessResults[3] == "r"):
        dataframe = dataframe.loc[dataframe["themes"].apply(lambda x: x.isdisjoint(guessThemes))]
    else:
        dataframe = dataframe.loc[dataframe["themes"].apply(lambda x: not (x.isdisjoint(guessThemes) or x == guessThemes))]
    
    if(guessResults[9] == "g"):
        dataframe = dataframe.loc[dataframe["franchises"] == guessFranchises]
    elif(guessResults[9] == "r"):
        dataframe = dataframe.loc[dataframe["franchises"].apply(lambda x: x.isdisjoint(guessFranchises))]
    else:
        dataframe = dataframe.loc[dataframe["franchises"].apply(lambda x: not (x.isdisjoint(guessFranchises) or x == guessFranchises))]
    
    if(guessCollection != 0):
        if(guessResults[10] == "g"):
            dataframe = dataframe.loc[dataframe["collection"] == guessCollection]
        else:
            dataframe = dataframe.loc[dataframe["collection"] != guessCollection]

    newCount = len(dataframe.index)
    if newCount == originalCount:
        dataframe = dataframe.loc[dataframe["value"] != guessResults[0]]
    p = newCount / originalCount
    entropy = log2(p) * (-1)
    print(f"Entropy: {entropy}")

    return dataframe

def guess(gameList: pd.DataFrame, guessId, genreFilter, themeFilter, yearFilter):
    newGameList = filter(gameList, guessId, genreFilter, themeFilter, yearFilter)
    newGameList["entropy"] = newGameList["value"].apply(lambda x: calculate_entropy(newGameList, x))

    return newGameList.sort_values(by=["entropy"], ascending=False)

def play_game(gameList: pd.DataFrame, chosenGameId):
    attempts = 0
    chosenGame = gameList.loc[gameList["value"] == chosenGameId]
    
    chosenGameYear = chosenGame.iat[0,2]
    chosenGameGenres = chosenGame.iat[0,3]
    chosenGameThemes = chosenGame.iat[0,4]

    while attempts < 10 and len(gameList.index) > 1:
        print(f"Attempt {attempts+1}: {gameList.iat[0,1]}")
        bestGameId = gameList.iat[0,0]
        bestGameYear = gameList.iat[0,2]
        bestGameGenres = gameList.iat[0,3]
        bestGameThemes = gameList.iat[0,4]


        genreFilter = ""
        themeFilter = ""
        yearFilter = ""

        if(chosenGameYear == bestGameYear):
            yearFilter = "="
        elif(chosenGameYear < bestGameYear):
            yearFilter = "<"
        else:
            yearFilter = ">"

        if(bestGameGenres == chosenGameGenres):
            genreFilter = "g"
        elif(bestGameGenres.isdisjoint(chosenGameGenres)):
            genreFilter = "r"
        else:
            genreFilter = "y"

        if(bestGameThemes == chosenGameThemes):
            themeFilter = "g"
        elif(bestGameThemes.isdisjoint(chosenGameThemes)):
            themeFilter = "r"
        else:
            themeFilter = "y"
        
        newGameList = guess(gameList, bestGameId, genreFilter, themeFilter, yearFilter)
        print("Infromation acquired on attempt:",str(log2(len(gameList.index) / len(newGameList.index))))
        attempts += 1
        gameList = newGameList
        
    if len(gameList.index) > 1:
        print(f"failed to narrow down game {chosenGameId} after {attempts} attempts")
        return (0, attempts)
    elif len(gameList.index) == 0:
        print(f"no games left for {chosenGameId} after {attempts} attempts")
        return (1, attempts)
    elif gameList.iat[0,0] != chosenGameId:
        print(f"guessed wrong game ({gameList.iat[0,1]}) insted of {chosenGameId} after {attempts} attempts")
        return (2, attempts)
    else:
        print(f"correctly guessed game ({gameList.iat[0,1]}) after {attempts} attempts")
        return (3, attempts)



def main():
    print("Loading data from JSON")
    gameList = pd.read_json("finalList.json")
    #gameList[["platforms", "genres", "companies", "engines", "modes", "perspectives", "themes", "franchises"]] = gameList[["platforms", "genres", "companies", "engines", "modes", "perspectives", "themes", "franchises"]].apply(set)
    gameList["platforms"] = gameList["platforms"].apply(set)
    gameList["genres"] = gameList["genres"].apply(set)
    gameList["companies"] = gameList["companies"].apply(set)
    gameList["engines"] = gameList["engines"].apply(set)
    gameList["modes"] = gameList["modes"].apply(set)
    gameList["perspectives"] = gameList["perspectives"].apply(set)
    gameList["themes"] = gameList["themes"].apply(set)
    gameList["franchises"] = gameList["franchises"].apply(set)

    print("Welcome to the game guesser! Pick an option to start:")
    print("1: GameGuessr")
    print("2: Entropy Calculator")
    opt = int(input())
    if opt == 1:
        while True:
            guessResults = input("Type the results of the guess (id, platform, genre, themes, year, mode, engine, companies, perspective, franchise):\n").split(" ")
            gameList = filter(gameList, guessResults)
            print(gameList)
    else:
        print("Work in progress")
    # gameList = gameList.sort_values(by=["entropy"], ascending=False)
    # play_game(gameList, 2184)
    # game_results = gameList["value"].apply(lambda x: play_game(gameList, x))
    # game_results.to_json("gameResults.json", orient="records")
    # print("Information acquired:", str(log2(len(gameList.index) / len(newGameList.index))))
    # gameList = newGameList
    
    # gameList["entropy"] = gameList["value"].apply(lambda x: calculate_entropy(gameList, x))
    # print(gameList.sort_values(by=["entropy"], ascending=False))
    # gameList.to_json("entropyList.json", orient="records")
    


if __name__ == "__main__":
    main()