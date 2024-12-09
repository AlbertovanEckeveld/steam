import json
from operator import truediv

steamJsonBestandPath = "../../steam.json"

with open(steamJsonBestandPath, "r") as steamData:
    steamData = json.load(steamData)



def zoekSpelOpNaam(spelNaam):
    returnWaarde = None

    for spel in steamData:
        if spel["name"].lower() == spelNaam.lower():
            returnWaarde = spel


    return returnWaarde



print(zoekSpelOpNaam("Garry's Mod"))




def getAlleSpellenVanOntwikkelaar(ontwikkelaar):
    resultaat = []
    for spel in steamData:
        if spel["developer"].lower() == ontwikkelaar.lower():
            resultaat.append(spel["name"])
    return resultaat



def getAlleSpellenVanUitgever(uitgever):
    resultaat = []
    for spel in steamData:
        if spel["publisher"].lower() == uitgever.lower():
            resultaat.append(spel["name"])
    return resultaat

def getGemiddeldeSpeeltijd(spelNaam):

    returnWaarde = None

    for spel in steamData:
        if spel["name"].lower() == spelNaam.lower():
            returnWaarde = spel["average_playtime"]

    return returnWaarde


print(getGemiddeldeSpeeltijd("Garry's Mod"))


def getAlleSpellenMetCategorie(categorie):
    resultaat = []
    for spel in steamData:
        lijstMetCategorieenvanSpel  = spel["categories"].split(";")
        for cat in lijstMetCategorieenvanSpel:
            if categorie.lower() == cat.strip().lower():
                resultaat.append(spel["name"])
    return resultaat


def getAlleSpellenOnderPrijs(maxPrijs):

    resultaat = []
    for spel in steamData:
        if spel["price"] <= maxPrijs:
            resultaat.append(spel["name"])
    return resultaat


def getAlleSpellenOpPlatform(platform): #Met platform wordt besturingssysteem bedoeld
    resultaat = []
    for spel in steamData:
        if platform.lower() in spel["platforms"].lower():
            resultaat.append(spel["name"])
    return resultaat


def getAlleSpellenMetGenre(genre):

    resultaat = []

    for spel in steamData:
        if genre.lower() in spel["genres"].lower():
            resultaat.append(spel["name"])

    return resultaat
