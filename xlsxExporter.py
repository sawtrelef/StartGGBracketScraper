import xlsxwriter

## namesdictionary example
#                          key-'Hungrybox':
#                               key-'melee-singles':(TotalSets, Set Wins, Total Games, Game Wins, DQs)
#                               key-'ultimate-singles':(DATA)

#namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)


#playersdictionary example
#       Key-'Hungrybox':
#               PlayerObject:
#                        opponents = {dictionary}
#                               #key-'melee-singles': {dict}
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                #key-'ultimate-singles':
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#
#playerdictionary[name].opponents[game][opponent] = (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)

def exportToxlsx(namesdictionary, playersdictionary, filetitle='default'):
    workbook = xlsxwriter.Workbook(filetitle+'.xlsx')
    gamenameworksheets = {}
    gamesetdict = {}
    gamematchdict = {}

    for name in namesdictionary:
        for game in namesdictionary[name]:
            if str(game + ' Set Records') not in gamenameworksheets:
                worksheet = workbook.add_worksheet(game + ' Set Records')
                gamenameworksheets[str(game + ' Set Records')] = worksheet
                gamenameworksheets[str(game + ' Set Records')].write(0,0, game)
                gamenameworksheets[str(game + ' Set Records')].write(1,0,'Competitor')
                gamenameworksheets[str(game + ' Set Records')].write(1,1,'Compiled Record')
                gamenameworksheets[str(game + ' Set Records')].write(1, 2, 'Wins')
                gamenameworksheets[str(game + ' Set Records')].write(1, 3, 'Losses')
                gamenameworksheets[str(game + ' Set Records')].write(1, 4, 'DQs')
                gamesetdict[game] = {}

            # namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)

            gamesetdict[str(game)][name] = (str(str(namesdictionary[name][game][1]) + ' - ' + str(namesdictionary[name][game][0]-namesdictionary[name][game][1])), str(namesdictionary[name][game][1]), str(namesdictionary[name][game][0]-namesdictionary[name][game][1]), str(namesdictionary[name][game][4]))


            # namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)
            if str(game + ' Match Records') not in gamenameworksheets:
                worksheet = workbook.add_worksheet(game + ' Match Records')
                gamenameworksheets[str(game + ' Match Records')] = worksheet
                gamenameworksheets[str(game + ' Match Records')].write(0,0, game)
                gamenameworksheets[str(game + ' Match Records')].write(1,0,'Competitor')
                gamenameworksheets[str(game + ' Match Records')].write(1,1,'Compiled Record')
                gamenameworksheets[str(game + ' Match Records')].write(1, 2, 'Wins')
                gamenameworksheets[str(game + ' Match Records')].write(1, 3, 'Losses')
                gamenameworksheets[str(game + ' Match Records')].write(1, 4, 'DQs')
                gamematchdict[game] = {}

            gamematchdict[str(game)][name] = (str(namesdictionary[name][game][3])+' - '+str(namesdictionary[name][game][2]-namesdictionary[name][game][3]), str(namesdictionary[name][game][3]), str(namesdictionary[name][game][2]-namesdictionary[name][game][3]), str(namesdictionary[name][game][4]))

    for game in gamesetdict:
        row = 2
        for name in gamesetdict[game]:
            gamenameworksheets[str(game+ ' Set Records')].write(row,0,name)
            gamenameworksheets[str(game+' Set Records')].write(row, 1, gamesetdict[game][name][0])
            gamenameworksheets[str(game + ' Set Records')].write(row, 2, gamesetdict[game][name][1])
            gamenameworksheets[str(game + ' Set Records')].write(row, 3, gamesetdict[game][name][2])
            gamenameworksheets[str(game + ' Set Records')].write(row, 4, gamesetdict[game][name][3])

            gamenameworksheets[str(game + ' Match Records')].write(row, 0, name)
            gamenameworksheets[str(game + ' Match Records')].write(row, 1, gamematchdict[game][name][0])
            gamenameworksheets[str(game + ' Match Records')].write(row, 2, gamematchdict[game][name][1])
            gamenameworksheets[str(game + ' Match Records')].write(row, 3, gamematchdict[game][name][2])
            gamenameworksheets[str(game + ' Match Records')].write(row, 4, gamematchdict[game][name][3])

            row = row + 1

    workbook.close()

