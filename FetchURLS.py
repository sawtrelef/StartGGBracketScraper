import requests
from bs4 import BeautifulSoup

URL1 = "https://www.start.gg/tournament/arcade-time-knockout-smash-brothers-tournament-with-hungrybox-2/event/ultimate-singles/brackets"

def fetchURLS(URL):
    listofURL = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all("div", class_="content-sggXIgPt")
    for link in links:
        links = link.find_all("a", href=True)
    return listofURL

list = fetchURLS(URL1)

print("goodbye")
quit()