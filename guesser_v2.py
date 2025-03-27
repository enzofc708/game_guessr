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


def filter(dataframe: pd.DataFrame, guessId, genreFilter, themeFilter, yearFilter):
    guess = dataframe.loc[dataframe["value"] == guessId]
    originalCount = len(dataframe.index)
    #print(guess)
    guessYear = guess.iat[0,2]
    guessGenres = guess.iat[0,3]
    guessThemes = guess.iat[0,4]
    

    if(yearFilter == "="):
        dataframe = dataframe.loc[dataframe["year"] == guessYear]
    elif(yearFilter == ">"):
        dataframe = dataframe.loc[dataframe["year"] > guessYear]
    else:
        dataframe = dataframe.loc[dataframe["year"] < guessYear]
        
    if(genreFilter == "g"):
        dataframe = dataframe.loc[dataframe["genres"] == guessGenres]
    elif(genreFilter == "r"):
        dataframe = dataframe.loc[dataframe["genres"].apply(lambda x: x.isdisjoint(guessGenres))]
    else:
        dataframe = dataframe.loc[dataframe["genres"].apply(lambda x: not (x.isdisjoint(guessGenres) or x == guessGenres))]

    if(themeFilter == "g"):
        dataframe = dataframe.loc[dataframe["themes"] == guessThemes]
    elif(themeFilter == "r"):
        dataframe = dataframe.loc[dataframe["themes"].apply(lambda x: x.isdisjoint(guessThemes))]
    else:
        dataframe = dataframe.loc[dataframe["themes"].apply(lambda x: not (x.isdisjoint(guessThemes) or x == guessThemes))]
    
    newCount = len(dataframe.index)
    if newCount == originalCount:
        dataframe = dataframe.loc[dataframe["value"] != guessId]

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
    # print("Loading data from JSON")
    # gameList = pd.read_json("entropyList.json")
    # gameList["genres"] = gameList["genres"].apply(set)
    # gameList["themes"] = gameList["themes"].apply(set)
    # gameList = gameList.sort_values(by=["entropy"], ascending=False)
    # play_game(gameList, 2184)
    # game_results = gameList["value"].apply(lambda x: play_game(gameList, x))
    # game_results.to_json("gameResults.json", orient="records")

    while True:
        guessResults = input("Type the results of the guess (platform, genre, themes, year, mode, engine, companies, perspective, franchise):\n").split(" ")
        
        newGameList = filter(guessResults)
        
        print(newGameList)
        # print("Information acquired:", str(log2(len(gameList.index) / len(newGameList.index))))
        # gameList = newGameList
    
    # gameList["entropy"] = gameList["value"].apply(lambda x: calculate_entropy(gameList, x))
    # print(gameList.sort_values(by=["entropy"], ascending=False))
    # gameList.to_json("entropyList.json", orient="records")
    


if __name__ == "__main__":
    main()