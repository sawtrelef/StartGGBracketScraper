import requests
from bs4 import BeautifulSoup

def fetchURLS(URL):
    listofURL = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all("div", class_="content-sggXIgPt")
    for link in links:
        links = link.find_all("a", href=True)
    return listofURL

