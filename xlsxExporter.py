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

def findsheet(workbook,sheetlist,cleanname,player):
    modifier = 0
    activesheet = sheetlist[cleanname]
    while activesheet.table[0][0] != player:
        modifier = modifier+1
        cleanname = cleanname + '-' + str(modifier)
        if cleanname not in sheetlist:
            sheetlist[cleanname] = workbook.add_worksheet(cleanname)
            sheetlist[cleanname].write(0,0, str(player))
            activesheet = sheetlist[cleanname]
            break
        else:
            activesheet = sheetlist[cleanname]
    return activesheet


def exportToxlsx(namesdictionary, playersdictionary, tournamentdictionary, filetitle='default'):
    workbook = xlsxwriter.Workbook(filetitle+'.xlsx')
    gamenameworksheets = {}
    gamesetdict = {}
    gamematchdict = {}
    tournamentsheets= {}
    playersheets = {}


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
    tournamentcount = 1
    tournamentnamelist = {}
    for tournament in tournamentdictionary:
        if tournament not in tournamentsheets:
            tournamentsheets[tournament] = workbook.add_worksheet(str("Tournament " + str(tournamentcount)))
            tournamentcount = tournamentcount +1
            tournamentnamelist[tournament] = []
        column = 0
        for game in tournamentdictionary[tournament]:
            tournamentsheets[tournament].write(0,column, str(game))
            tournamentsheets[tournament].write(0,column+1, "Record")
            row = 1
            for name in tournamentdictionary[tournament][game]:
                tournamentsheets[tournament].write(row,column, name)
                tournamentsheets[tournament].write(row,column+1, str(tournamentdictionary[tournament][game][name]))
                row = row+1
                if name not in tournamentnamelist[tournament]:
                    tournamentnamelist[tournament].append(name)

            column = column+2

        tournamentsheets[tournament].write(0,column, "Attendees List")
        row = 1
        for name in tournamentnamelist[tournament]:
            tournamentsheets[tournament].write(row,column, name)
            row = row+1

    for player in playersdictionary:
        opponentdict = {}
        cleanname = player.upper()

        for item in ['[', ']', ':', '*', '?', '/', '\\']:
            if item in cleanname:
                cleanname = cleanname.replace(item, '!')
        if cleanname not in playersheets:
            playersheets[cleanname] = workbook.add_worksheet(cleanname)
            playersheets[cleanname].write(0,0, str(player))
            activesheet = playersheets[cleanname]
        else:
            activesheet = findsheet(workbook,playersheets, cleanname, player)





        column = 0

        for game in playersdictionary[player].opponents:
            activesheet.write(1,column,game)
            activesheet.write(1,column+1,"record")
            row = 2
            for opponent in playersdictionary[player].opponents[game]:
                if opponent not in opponentdict:
                    opponentdict[opponent] = 0,0,0,0,0,0,0
                opponentdict[opponent] = playersdictionary[player].opponents[game][opponent][0] + opponentdict[opponent][0],playersdictionary[player].opponents[game][opponent][1] + opponentdict[opponent][1],playersdictionary[player].opponents[game][opponent][2] + opponentdict[opponent][2],playersdictionary[player].opponents[game][opponent][3] + opponentdict[opponent][3],playersdictionary[player].opponents[game][opponent][4] + opponentdict[opponent][4],playersdictionary[player].opponents[game][opponent][5] + opponentdict[opponent][5],playersdictionary[player].opponents[game][opponent][6] + opponentdict[opponent][6]
                activesheet.write(row,column,opponent)
                activesheet.write(row,column+1,str(playersdictionary[player].opponents[game][opponent]))
                row = row+1
            column = column+2
        activesheet.write(1,column, "Opponent")
        activesheet.write(1,column+1, "Overall Record")
        row = 2
        for opponent in opponentdict:
            activesheet.write(row, column, opponent)
            activesheet.write(row, column + 1, str(opponentdict[opponent]))
            row = row+1


    print("Done")



    workbook.close()

