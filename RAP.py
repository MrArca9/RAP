import requests
import re
from re import RegexFlag
import time
import datetime
import json
import urllib
import html
from html.parser import HTMLParser
ParsedAnime =[]
from urllib.parse import unquote
def cleanUp(url):
    try:
        return unquote(url, errors='strict')
    except UnicodeDecodeError:
        return unquote(url, encoding='latin-1')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
class Show(object):
    def __init__(self):
        self.Name = ""
        self.Desc = ""
        self.Rating = 0
        self.EndDate = ""
        self.ImageUrl = ""
        self.Genres = []

class Seasons(object):
    def __init__(self):
        self.Version = str(datetime.datetime.now().timestamp())
        self.Winter = []
        self.Spring = []
        self.Summer = []
        self.Fall = []
    def addShowToWinter(self, Show):
        self.Winter.append(Show)
    def addShowToSpring(self, Show):
        self.Spring.append(Show)
    def addShowToSummer(self, Show):
        self.Summer.append(Show)
    def addShowToFall(self, Show):
        self.Fall.append(Show)

i = 1
AnimeSeason = Seasons()
while(i < 5):
    year = str(datetime.datetime.now().year)
    if(i == 2):
        season = 'spring'
    if(i == 3):
        season = 'summer'
    if(i == 4):
        season = 'fall'
    if(i == 1):
        season = 'winter'
    url = 'https://myanimelist.net/anime/season/'+year+'/'+season
    i = i + 1
    Anime9Plus = {}
    Anime9PlusSorted = []
    Anime89 = {}
    Anime89Sorted = []
    Anime78 = {}
    Anime78Sorted = []
    Anime67 = {}
    Anime67Sorted = []
    Anime56 = {}
    Anime56Sorted = []
    Anime45 = {}
    Anime45Sorted = []
    Anime34 = {}
    Anime34Sorted = []
    Anime23 = {}
    Anime23Sorted = []
    Anime12 = {}
    Anime12Sorted = []
    r = requests.get(url)
    if(r.status_code != 200):
        print("ERROR: SEASON " + season.upper() + " DOESN'T EXIST")
        continue
    response0 = r.content
    response = str(response0, 'utf-8', errors='replace')
    taggedList = re.findall('<div class=\"seasonal-anime js-seasonal-anime\".*?</div>', response, flags= RegexFlag.DOTALL)
    for tag in taggedList:
        while True:
            AnimeName = cleanUp(re.findall('link-title\">.*?</a>', tag)[0].replace('link-title">','').replace('</a>', ''))
            AnimeUrl = cleanUp(re.findall('<a href=".*? ', tag)[0].replace('<a href="','').replace('/video"',''))
            if(AnimeName in ParsedAnime):
                print('***SKIPPING PARSED ANIME '+AnimeName+'***')
                break
            response = str(requests.get(AnimeUrl).content, 'utf-8', errors='replace')
            time.sleep(3)
            if len(response) < 20:
                ## Probably "Too Many Requests"
                time.sleep(5)
                continue
            Aired = re.findall('<span class="dark_text">Aired:</span>.*?</div>',response, flags=RegexFlag.DOTALL)[0].replace('\\n','').replace('<span class="dark_text">Aired:</span>','').replace('</div>','')
            try:
                Rating = re.findall('<span itemprop="ratingValue">.*?</span>',response, flags=RegexFlag.DOTALL)[0].replace('\\n','').replace('<span itemprop="ratingValue">','').replace('</span>','')
            except:
                Rating = re.findall('<div class="po-r js-statistics-info di-ib" data-id="info1">.*?</div>',response, flags=RegexFlag.DOTALL)[0]
                Rating = re.findall('<span>.*?</span>', Rating, flags=RegexFlag.DOTALL)[0].replace('<span>','').replace('</span>','')
            try:
                reImageString = '<img src="https://myanimelist.cdn-dena.com/images/anime/.*?itemprop="image"'
                ImageUrl = re.findall(reImageString, response, flags=RegexFlag.DOTALL)[0].split("<img src=\"")[1].split('"')[0]
            except:
                try:
                    reImageString = '<img src="https://cdn.myanimelist.net/images/anime/.*?itemprop="image"'
                    ImageUrl = re.findall(reImageString, response, flags=RegexFlag.DOTALL)[0].split("<img src=\"")[1].split('"')[0]
                except:
                    print("ERROR GETTING IMAGE URL")
                    ImageUrl = ""
            try:
                desc = strip_tags(re.findall('<span itemprop="description">.*?</span>', response, flags=RegexFlag.DOTALL)[0].replace('<span itemprop="description">','').replace('</span>','')).replace("\\n",'').replace('\\r','').replace('[Written by MAL Rewrite]','')
            except:
                print("ERROR GETTING DESC")
                desc = "None"
            try:
                genresCompressed =re.findall('<span class=\"dark_text\">Genres.*?</div>', response, flags=RegexFlag.DOTALL)[0]
                animeType = re.findall('>.*?<', re.findall('<span class=\"dark_text\">Type:.*?</div>', response, flags=RegexFlag.DOTALL)[0], flags=RegexFlag.DOTALL)[2].replace('>','').replace('<','')
                genreList = re.findall('title=.*?\">', genresCompressed, flags=RegexFlag.DOTALL)
                genreListClean = []
                genreListClean.append(animeType)
                for stringValue in genreList:
                    stringValue = stringValue.replace('title="','').replace('">','')
                    genreListClean.append(stringValue)

            except:
                print("ERROR GETTING GENRES")
                genreListClean = []
            if('N/A' not in Rating):
                Rating = float(Rating)
            else:
                Rating = 1.00
            Aired = Aired.strip(' \t\n\r')
            StartAired = Aired.split(' to ')[0]
            try:
                EndAired = Aired.split(' to ')[1]   
            except:
                 EndAired = Aired.split(' to ')[0]   
            if('Currently Airing' in response):
                print('SILL AIRING: '+AnimeName+' ('+Aired+')')
                ParsedAnime.append(AnimeName)
                break
            elif('Finished Airing' in response):
                AnimeName = AnimeName.replace('&#039;',"'")
                try:
                    DT_EndAired = datetime.datetime.strptime(EndAired, '%b %d, %Y')
                except:
                    DT_EndAired = datetime.datetime.strptime(EndAired, '%b, %Y')
                show = Show()
                show.Name = AnimeName
                show.EndDate = EndAired
                show.ImageUrl = ImageUrl
                show.Desc = desc
                show.Genres = genreListClean
                if(Rating > 9):
                    Anime9Plus[AnimeName] = DT_EndAired
                    show.Rating = 10
                elif(Rating > 8):
                    Anime89[AnimeName] = DT_EndAired
                    show.Rating = 9
                elif(Rating > 7):
                    Anime78[AnimeName] = DT_EndAired
                    show.Rating = 8
                elif(Rating > 6):
                    Anime67[AnimeName] = DT_EndAired
                    show.Rating = 7
                elif(Rating > 5):
                    Anime56[AnimeName] = DT_EndAired
                    show.Rating = 6
                elif(Rating > 4):
                    Anime45[AnimeName] = DT_EndAired
                    show.Rating = 5
                elif(Rating > 3):
                    Anime34[AnimeName] = DT_EndAired
                    show.Rating = 4
                elif(Rating > 2):
                    Anime23[AnimeName] = DT_EndAired
                    show.Rating = 3
                elif(Rating > 1):
                    Anime12[AnimeName] = DT_EndAired
                    show.Rating = 2
                print('** COMPLETED **: '+ AnimeName+' ('+Aired+')')
                ParsedAnime.append(AnimeName)
                if season == "spring":
                    AnimeSeason.addShowToSpring(show.__dict__)
                if season == "winter":
                    AnimeSeason.addShowToWinter(show.__dict__)
                if season == "summer":
                    AnimeSeason.addShowToSummer(show.__dict__)
                if season == "fall":
                    AnimeSeason.addShowToFall(show.__dict__)
                with open("AnimeDatabase.json", "w+") as text_file:
                    text_file.write(json.dumps(AnimeSeason.__dict__))
                break
            else:
                print('NOT AIRED: '+AnimeName+' ('+Aired+')')
                ParsedAnime.append(AnimeName)
                break
    Anime9PlusSorted = sorted(Anime9Plus, key=Anime9Plus.get, reverse=True)
    Anime89Sorted = sorted(Anime89,   key=Anime89.get, reverse=True)
    Anime78Sorted = sorted(Anime78,   key=Anime78.get, reverse=True)
    Anime67Sorted = sorted(Anime67,   key=Anime67.get, reverse=True)
    Anime56Sorted = sorted(Anime56,   key=Anime56.get, reverse=True)
    Anime45Sorted = sorted(Anime45,   key=Anime45.get, reverse=True)
    Anime34Sorted = sorted(Anime34,   key=Anime34.get, reverse=True)
    Anime23Sorted = sorted(Anime23,   key=Anime23.get, reverse=True)
    Anime12Sorted = sorted(Anime12,   key=Anime12.get, reverse=True)
    with open(season+' Anime.txt','a+') as f:
        pass
    with open(season+' Anime.txt', 'r+') as f:
        f.write(season+' '+year+' list!\nAnime is ordered in rating, followed by most recently completed in that rating.\n\n')
        f.write('9+:\n')
        for anime in Anime9PlusSorted:
            f.write(anime+'\n')
        f.write('\n8:\n')
        for anime in Anime89Sorted:
            f.write(anime+'\n')
        f.write('\n7:\n')
        for anime in Anime78Sorted:
            f.write(anime+'\n')
        f.write('\n6:\n')
        for anime in Anime67Sorted:
            f.write(anime+'\n')
        f.write('\n5:\n')
        for anime in Anime56Sorted:
            f.write(anime+'\n')
        f.write('\n4:\n')
        for anime in Anime45Sorted:
            f.write(anime+'\n')
        f.write('\n3:\n')
        for anime in Anime34Sorted:
            f.write(anime+'\n')
        f.write('\n2:\n')
        for anime in Anime23Sorted:
            f.write(anime+'\n')
        f.write('\n1:\n')
        for anime in Anime12Sorted:
            f.write(anime+'\n')