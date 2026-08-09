from BracketLinkPuller import fetchBracketURLS

def gatherURLs(URLLIST = False,smash=False):


    #while not done:
        #eventlist = pygame.event.get()
        #for event in eventlist:
            #if event.type == pygame.QUIT:
                #done = True
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print("you clicked something")
                #position = pygame.mouse.get_pos()
                #for clickable in clickableobjectlist:
                    #if clickcheck(position,clickable):
                        #print("we doin' stuff")
            #if event.type == pygame.VIDEORESIZE:
                #newWidth, newHeight = event.dict['size']
                #backgroundrect.width = newWidth
                #backgroundrect.height = newHeight
                #width = newWidth
                #height = newHeight
                #display = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)
            #if done:
                #break
        #print("in gather url phase")
        #pygame.draw.rect(display, (0, 0, 0), backgroundrect)
        #pygame.display.update()

    if URLLIST == False:
        urlfile = open('urllist.txt')
        urltext = urlfile.read()
        URLLIST = urltext.splitlines()
        if urlfile != False:
            urlfile.close()
            del urlfile
        if urltext != False:
            del urltext

    BRACKETURLLIST = []
    for URL in URLLIST:
        URLSPLITS = URL.split('/')
        gamesplit = URLSPLITS.index('tournament')
        tournamentname = URLSPLITS[gamesplit+1]
        if 'brackets' in URLSPLITS:
            if URLSPLITS[len(URLSPLITS)-1] != 'brackets':
                BRACKETURLLIST.append(URL)
                continue
        listofbrackets = fetchBracketURLS(URL,smash)
        for bracket in listofbrackets:
            BRACKETURLLIST.append(bracket)

    if URLLIST:
        del URLLIST
    return BRACKETURLLIST