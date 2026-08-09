import gc

import xlsxwriter

## namesdictionary example
#                          key-'Hungrybox':
#                               key-'melee-singles':(TotalSets, Set Wins, Total Games, Game Wins, DQs)
#                               key-'ultimate-singles':(DATA)

#namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)


#playersdictionary example
#       Key-'Hungrybox':
#               PlayerObject:
#                       [' opponents'] = {dictionary}
#                               #key-'melee-singles': {dict}
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                #key-'ultimate-singles':
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#                                        key-'OpponentName': (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)
#
#playerdictionary[name]['.opponents'][game][opponent] = (SetsPlayed, SetsWon, Sets Lost, GamesPlayed, GamesWon, GamesLost, DQ)

def findsheet(workbooklist,sheetlist,cleanname,player):
    modifier = 0
    activesheet = sheetlist[cleanname]
    while activesheet.table[0][0] != player:
        modifier = modifier+1
        cleanname = cleanname + '-' + str(modifier)
        if cleanname not in sheetlist:
            sheetlist[cleanname] = workbooklist[len(workbooklist)-1].add_worksheet(cleanname)
            sheetlist[cleanname].write(0,0, str(player))
            activesheet = sheetlist[cleanname]
            break
        else:
            activesheet = sheetlist[cleanname]
    return activesheet

def findsheet2(workbooklist,sheetlist,cleanname,player,game):
    modifier = 0
    activesheet = sheetlist[cleanname]
    while activesheet.table[0][0] != player:
        modifier = modifier+1
        cleanname = cleanname + '-' + str(modifier)
        if cleanname not in sheetlist:
            sheetlist[cleanname] = workbooklist[game][len(workbooklist[game])-1].add_worksheet(cleanname)
            sheetlist[cleanname].write(0,0, str(player))
            activesheet = sheetlist[cleanname]
            break
        else:
            activesheet = sheetlist[cleanname]
    return activesheet


def exportToxlsx(namesdictionary, playersdictionary, tournamentdictionary, recentlist, projectpath='default' ):
    if projectpath != 'default':
        projectname = projectpath.split('\\')[2]


    workbook = xlsxwriter.Workbook(projectpath+'\\'+projectname+'.xlsx')
    gamenameworksheets = {}
    gamesetdict = {}
    gamematchdict = {}
    tournamentsheets= {}
    playersheets = {}
    playerlist = []


    for name in namesdictionary:
        for game in namesdictionary[name]:
            if game == 'super-smash-bros-ultimate-doubles':
                print("this is where problems start")

            recordname = game + ' Set Records'
            if game == "under-night-in-birth-ii-sys:celes":
                print("beep")
            if len(recordname) > 31:
                recordname = recordname.replace('-','')
                if len(recordname) > 31:
                    recordname = recordname[:31 - len(' Set Records')]
                    recordname = recordname + ' Set Records'
            if str(recordname) not in gamenameworksheets:
                worksheet = workbook.add_worksheet(recordname)
                gamenameworksheets[recordname] = worksheet
                gamenameworksheets[recordname].write(0,0, game)
                gamenameworksheets[recordname].write(1,0,'Competitor')
                gamenameworksheets[recordname].write(1,1,'Compiled Record')
                gamenameworksheets[recordname].write(1, 2, 'Wins')
                gamenameworksheets[recordname].write(1, 3, 'Losses')
                gamenameworksheets[recordname].write(1, 4, 'DQs')
                gamesetdict[game] = {}

            # namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)

            gamesetdict[str(game)][name] = (str(str(namesdictionary[name][game][1]) + ' - ' + str(namesdictionary[name][game][0]-namesdictionary[name][game][1])), str(namesdictionary[name][game][1]), str(namesdictionary[name][game][0]-namesdictionary[name][game][1]), str(namesdictionary[name][game][4]))


            # namesdictionary[name][game] = (TotalSets,SetWins,TotalGames,Gamewins,DQs)
            recordname = game + ' Match Records'
            if len(recordname) > 31:
                recordname = recordname.replace('-','')
                if len(recordname) > 31:
                    recordname = recordname[:31 - len(' Match Records')]
                    recordname = recordname + ' Match Records'
            if str(recordname) not in gamenameworksheets:
                worksheet = workbook.add_worksheet(recordname)
                gamenameworksheets[recordname] = worksheet
                gamenameworksheets[recordname].write(0,0, game)
                gamenameworksheets[recordname].write(1,0,'Competitor')
                gamenameworksheets[recordname].write(1,1,'Compiled Record')
                gamenameworksheets[recordname].write(1, 2, 'Wins')
                gamenameworksheets[recordname].write(1, 3, 'Losses')
                gamenameworksheets[recordname].write(1, 4, 'DQs')
                gamematchdict[game] = {}

            gamematchdict[str(game)][name] = (str(namesdictionary[name][game][3])+' - '+str(namesdictionary[name][game][2]-namesdictionary[name][game][3]), str(namesdictionary[name][game][3]), str(namesdictionary[name][game][2]-namesdictionary[name][game][3]), str(namesdictionary[name][game][4]))

    for game in gamesetdict:
        row = 2
        recordname = game + ' Set Records'
        if len(recordname) > 31:
            recordname = recordname.replace('-', '')
            if len(recordname) > 31:
                recordname = recordname[:31 - len(' Set Records')]
                recordname = recordname + ' Set Records'
        recordname2 = game + ' Match Records'
        if len(recordname2) > 31:
            recordname2 = recordname2.replace('-', '')
            if len(recordname2) > 31:
                recordname2 = recordname2[:31 - len(' Match Records')]
                recordname2 = recordname2 + ' Match Records'
        for name in gamesetdict[game]:
            gamenameworksheets[recordname].write(row,0,name)
            gamenameworksheets[recordname].write(row, 1, gamesetdict[game][name][0])
            gamenameworksheets[recordname].write(row, 2, int(gamesetdict[game][name][1]))
            gamenameworksheets[recordname].write(row, 3, int(gamesetdict[game][name][2]))
            gamenameworksheets[recordname].write(row, 4, int(gamesetdict[game][name][3]))

            gamenameworksheets[recordname2].write(row, 0, name)
            gamenameworksheets[recordname2].write(row, 1, gamematchdict[game][name][0])
            gamenameworksheets[recordname2].write(row, 2, int(gamematchdict[game][name][1]))
            gamenameworksheets[recordname2].write(row, 3, int(gamematchdict[game][name][2]))
            gamenameworksheets[recordname2].write(row, 4, int(gamematchdict[game][name][3]))

            row = row + 1
    tournamentcount = 1
    tournamentnamelist = {}
    for tournament in tournamentdictionary:
        if tournament not in tournamentsheets:
            tournamentsheets[tournament] = workbook.add_worksheet(str("Tournament " + str(tournamentcount)))
            tournamentsheets[tournament].write(0,0,tournament)
            tournamentcount = tournamentcount +1
            tournamentnamelist[tournament] = []
        column = 0
        for game in tournamentdictionary[tournament]:
            tournamentsheets[tournament].write(1,column, str(game))
            tournamentsheets[tournament].write(1,column+1, "Sets Played")
            tournamentsheets[tournament].write(1, column + 2, "Sets Won")
            tournamentsheets[tournament].write(1, column + 3, "Games Played")
            tournamentsheets[tournament].write(1, column + 4, "Games Won")
            tournamentsheets[tournament].write(1, column + 5, "Times DQ'd")
            row = 2
            for name in tournamentdictionary[tournament][game]:
                tournamentsheets[tournament].write(row,column, name)
                tournamentsheets[tournament].write(row,column+1, int(tournamentdictionary[tournament][game][name][0]))
                tournamentsheets[tournament].write(row, column + 2, int(tournamentdictionary[tournament][game][name][1]))
                tournamentsheets[tournament].write(row, column + 3, int(tournamentdictionary[tournament][game][name][2]))
                tournamentsheets[tournament].write(row, column + 4, int(tournamentdictionary[tournament][game][name][3]))
                tournamentsheets[tournament].write(row, column + 5, int(tournamentdictionary[tournament][game][name][4]))

                row = row+1
                if name not in tournamentnamelist[tournament]:
                    tournamentnamelist[tournament].append(name)

            column = column+7

        tournamentsheets[tournament].write(1,column, "Attendees List")
        row = 2
        for name in tournamentnamelist[tournament]:
            tournamentsheets[tournament].write(row,column, name)
            row = row+1

    gamedict = {}
    gamebooks = {}

    for player in playersdictionary:
        playerlist.append(player)
        for game in playersdictionary[player]['opponents']:
            if game not in gamedict:
                gamedict[game] = []
                gamebooks[game] = {}
            if player not in gamedict[game]:
                gamedict[game].append(player)

    for game in gamedict:
        gamedict[game].sort()

    playerlist.sort()
    playercount = 0
    workbookcount = 0
    playerworkbooks = {}
    playerworkbooks[0] = xlsxwriter.Workbook(projectpath+'\\'+projectname+"PlayerMasterData"+str(workbookcount)+".xlsx")

    for player in playerlist:
        playercount = playercount + 1
        workbookcount = int(playercount/255)
        if workbookcount not in playerworkbooks:
            playerworkbooks[workbookcount] = xlsxwriter.Workbook(projectpath+'\\'+projectname+"Players"+str(workbookcount)+".xlsx")
        opponentdict = {}
        cleanname = player.upper()

        for item in ['[', ']', ':', '*', '?', '/', '\\']:
            if item in cleanname:
                cleanname = cleanname.replace(item, '!')

        if cleanname[0] == '\'':
            cleanname = '!' + cleanname[1:]
        if cleanname[len(cleanname)-1] == '\'':
            cleanname = cleanname[:len(cleanname)-2] + '!'
        if len(cleanname) > 31:
            cleanname = cleanname[:31]
        if cleanname not in playersheets:
            playersheets[cleanname] = playerworkbooks[workbookcount].add_worksheet(cleanname)
            playersheets[cleanname].write(0,0, str(player))
            activesheet = playersheets[cleanname]
        else:
            activesheet = findsheet(playerworkbooks,playersheets, cleanname, player)

        column = 0
        for game in playersdictionary[player]['opponents']:
            activesheet.write(1,column,game)
            activesheet.write(1,column+1,"Sets Played")
            activesheet.write(1,column+2,"Sets Won")
            activesheet.write(1,column+3,"Sets Lost")
            activesheet.write(1,column+4,"Games Played")
            activesheet.write(1,column+5,"Games Won")
            activesheet.write(1, column + 6, "Games Lost")
            activesheet.write(1, column + 7, "DQ'd")

            row = 2
            for opponent in playersdictionary[player]['opponents'][game]:
                if opponent == 'TOURNAMENT_NAME' or opponent == 'TIME_STAMP' or opponent == 'PLACEMENT':
                    continue
                if opponent not in opponentdict:
                    opponentdict[opponent] = 0,0,0,0,0,0,0
                opponentdict[opponent] = playersdictionary[player]['opponents'][game][opponent][0] + opponentdict[opponent][0],playersdictionary[player]['opponents'][game][opponent][1] + opponentdict[opponent][1],playersdictionary[player]['opponents'][game][opponent][2] + opponentdict[opponent][2],playersdictionary[player]['opponents'][game][opponent][3] + opponentdict[opponent][3],playersdictionary[player]['opponents'][game][opponent][4] + opponentdict[opponent][4],playersdictionary[player]['opponents'][game][opponent][5] + opponentdict[opponent][5],playersdictionary[player]['opponents'][game][opponent][6] + opponentdict[opponent][6]
                activesheet.write(row,column,opponent)
                activesheet.write(row,column+1,int(playersdictionary[player]['opponents'][game][opponent][0]))
                activesheet.write(row, column + 2, int(playersdictionary[player]['opponents'][game][opponent][1]))
                activesheet.write(row, column + 3, int(playersdictionary[player]['opponents'][game][opponent][2]))
                activesheet.write(row, column + 4, int(playersdictionary[player]['opponents'][game][opponent][3]))
                activesheet.write(row, column + 5, int(playersdictionary[player]['opponents'][game][opponent][4]))
                activesheet.write(row, column + 6, int(playersdictionary[player]['opponents'][game][opponent][5]))
                activesheet.write(row, column + 7, int(playersdictionary[player]['opponents'][game][opponent][6]))
                row = row+1
            column = column+9
        activesheet.write(1,column, "Opponent")
        activesheet.write(1, column + 1, "Total Sets Played")
        activesheet.write(1, column + 2, "Total Sets won")
        activesheet.write(1, column + 3, "Total Sets Lost")
        activesheet.write(1, column + 4, "Total Games Played")
        activesheet.write(1, column + 5, "Total Games Won")
        activesheet.write(1, column + 6, "Total Games Lost")
        activesheet.write(1, column + 7, "Total Times DQ'd")
        row = 2
        for opponent in opponentdict:
            activesheet.write(row, column, opponent)
            activesheet.write(row, column + 1, int(opponentdict[opponent][0]))
            activesheet.write(row, column + 2, int(opponentdict[opponent][1]))
            activesheet.write(row, column + 3, int(opponentdict[opponent][2]))
            activesheet.write(row, column + 4, int(opponentdict[opponent][3]))
            activesheet.write(row, column + 5, int(opponentdict[opponent][4]))
            activesheet.write(row, column + 6, int(opponentdict[opponent][5]))
            activesheet.write(row, column + 7, int(opponentdict[opponent][6]))
            row = row+1
        column = column+9
        row = 1
        activesheet.write(0,column, "LAST SEEN")
        for game in playersdictionary[player]['opponents']:
            if game in recentlist:
                if player in recentlist[game]:
                    activesheet.write(row, column, str(game))
                    activesheet.write(row,column+1, str(recentlist[game][player]['TOURNAMENT_NAME']))
                    activesheet.write(row,column+2, str('PLACEMENT'))
                    activesheet.write(row,column+3, str(recentlist[game][player]['PLACEMENT']))
                    row = row + 1
                    activesheet.write(row, column, "Opponent")
                    activesheet.write(row, column + 1, "Total Sets Played")
                    activesheet.write(row, column + 2, "Total Sets won")
                    activesheet.write(row, column + 3, "Total Sets Lost")
                    activesheet.write(row, column + 4, "Total Games Played")
                    activesheet.write(row, column + 5, "Total Games Won")
                    activesheet.write(row, column + 6, "Total Games Lost")
                    activesheet.write(row, column + 7, "Total Times DQ'd")
                    row = row+1
                    for opponent in recentlist[game][player]:
                        if opponent == 'TOURNAMENT_NAME' or opponent == 'TIME_STAMP' or opponent == 'PLACEMENT':
                            continue
                        activesheet.write(row,column, opponent)
                        activesheet.write(row, column + 1, recentlist[game][player][opponent][0])
                        activesheet.write(row, column + 2, recentlist[game][player][opponent][1])
                        activesheet.write(row, column + 3, recentlist[game][player][opponent][2])
                        activesheet.write(row, column + 4, recentlist[game][player][opponent][3])
                        activesheet.write(row, column + 5, recentlist[game][player][opponent][4])
                        activesheet.write(row, column + 6, recentlist[game][player][opponent][5])
                        activesheet.write(row, column + 7, recentlist[game][player][opponent][6])
                        row = row+1
                row = row + 1

        column = column + 10
        row = 2
        activesheet.write(1, column, "TIMES ATTENDED")
        count = 0
        attendencelist = []
        for tournament in tournamentdictionary:
            breakcheck = False
            for game in tournamentdictionary[tournament]:
                if breakcheck == False:
                    if player in tournamentdictionary[tournament][game]:
                        count = count+1
                        breakcheck == True
                        attendencelist.append(tournament)
                        break
                else:
                    break
        activesheet.write(1, column+1,count)
        for tournament in attendencelist:
            activesheet.write(row,column,str(tournament))
            row = row+1



    for game in gamedict:
        playercount = 0
        workbookcount = 0
        gamebooks[game][0] = xlsxwriter.Workbook(projectpath+'\\'+projectname+str(game)+"PlayerData"+str(workbookcount)+".xlsx")
        playersheets = {}

        for player in gamedict[game]:
            playercount = playercount+1
            workbookcount = int(playercount/256)
            if workbookcount not in gamebooks[game]:
                gamebooks[game][workbookcount] = xlsxwriter.Workbook(projectpath+'\\'+projectname+str(game) + "PlayerData" + str(workbookcount) + ".xlsx")
            cleanname = player.upper()

            for item in ['[', ']', ':', '*', '?', '/', '\\']:
                if item in cleanname:
                    cleanname = cleanname.replace(item, '!')
            if cleanname[0] == '\'':
                cleanname = '!' + cleanname[1:]
            if cleanname[len(cleanname)-1] == '\'':
                cleanname = cleanname[:len(cleanname)-2] + '!'
            if len(cleanname) > 31:
                cleanname = cleanname[:31]

            if cleanname not in playersheets:
                playersheets[cleanname] = gamebooks[game][workbookcount].add_worksheet(cleanname)
                playersheets[cleanname].write(0, 0, str(player))
                activesheet = playersheets[cleanname]
            else:
                activesheet = findsheet2(gamebooks, playersheets, cleanname, player, game)

            column = 0
            activesheet.write(1, column, game)
            activesheet.write(1, column + 1, "Sets Played")
            activesheet.write(1, column + 2, "Sets Won")
            activesheet.write(1, column + 3, "Sets Lost")
            activesheet.write(1, column + 4, "Games Played")
            activesheet.write(1, column + 5, "Games Won")
            activesheet.write(1, column + 6, "Games Lost")
            activesheet.write(1, column + 7, "DQ'd")
            row = 2
            for opponent in playersdictionary[player]['opponents'][game]:
                if opponent == 'TOURNAMENT_NAME' or opponent == 'TIME_STAMP' or opponent == 'PLACEMENT':
                    continue
                activesheet.write(row, column, opponent)
                activesheet.write(row, column + 1, int(playersdictionary[player]['opponents'][game][opponent][0]))
                activesheet.write(row, column + 2, int(playersdictionary[player]['opponents'][game][opponent][1]))
                activesheet.write(row, column + 3, int(playersdictionary[player]['opponents'][game][opponent][2]))
                activesheet.write(row, column + 4, int(playersdictionary[player]['opponents'][game][opponent][3]))
                activesheet.write(row, column + 5, int(playersdictionary[player]['opponents'][game][opponent][4]))
                activesheet.write(row, column + 6, int(playersdictionary[player]['opponents'][game][opponent][5]))
                activesheet.write(row, column + 7, int(playersdictionary[player]['opponents'][game][opponent][6]))
                row = row + 1


    print("Done")



    workbook.close()
    for workbook in playerworkbooks:
        playerworkbooks[workbook].close()

    for game in gamebooks:
        for workbook in gamebooks[game]:
            gamebooks[game][workbook].close()

    del activesheet
    del attendencelist
    del breakcheck
    del cleanname
    del column
    del count
    del game
    del gamebooks
    del gamedict
    del gamematchdict
    del gamenameworksheets
    del gamesetdict
    del item
    del name
    del opponent
    del opponentdict
    del player
    del playercount
    del playerlist
    del playersheets
    del playerworkbooks
    del projectname
    del recordname
    del recordname2
    del row
    del tournament
    del tournamentcount
    del tournamentnamelist
    del tournamentsheets
    del workbook
    del workbookcount
    del worksheet
    gc.collect()



    #del cleanname
    #del column
    #del filetitle
    #del game
    #del gamebooks
    #del gamedict
    #del gamematchdict
    #del gamenameworksheets
    #del gamesetdict
    #del item
    #del name
    #del namesdictionary
    #del opponent
    #del opponentdict
    #del player
    #del playercount
    #del playerlist
    #del playersdictionary
    #del playersheets
    #del playerworkbooks
    #del recordname
    #del recordname2
    #del row
    #del tournament
    #del tournamentcount
    #del tournamentdictionary
    #del tournamentnamelist
    #del tournamentsheets
    #del workbook
    #del workbookcount
    #del worksheet


