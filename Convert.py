import json

class Show(object):
    def __init__(self):
        self.Name = ""
        self.Desc = ""
        self.Rating = 0
        self.EndDate = ""

class Seasons(object):
    def __init__(self):
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
## MUST ADD SHOWS USING show.__dict__
## MUST CONVERT JSON STRING USING seasons.__dict__
winterString = ""
springString = ""
summerString = ""
fallString = ""
with open('winter Anime.txt', 'r') as myfile:
    winterString=myfile.read()
with open('spring Anime.txt', 'r') as myfile:
    springString=myfile.read()
with open('summer Anime.txt', 'r') as myfile:
    summerString=myfile.read()
with open('fall Anime.txt', 'r') as myfile:
    fallString=myfile.read()
GlobalString = winterString + "\n SPRINGSHOWSSTARTHERE \n" + springString + "\n SUMMERSHOWSSTARTHERE \n" + summerString + "\n FALLSHOWSSTARTHERE \n" + fallString
showStringRating = 0
currentSeason = "Winter"
seasons = Seasons()
for showString in GlobalString.splitlines():
    show = Show()
    showString = showString.strip()
    if(showString == '\n'):
        continue
    if showString.strip() == "":
        continue
    if showString == '9+:':
        showStringRating = 9
        continue
    if showString == '8:':
        showStringRating = 8
        continue
    if showString == '7:':
       showStringRating = 7
       continue
    if showString == '6:':
       showStringRating = 6
       continue
    if showString == '5:':
        showStringRating = 5
        continue
    if showString == '4:':
       showStringRating = 4
       continue
    if showString == '3:':
        showStringRating = 3
        continue
    if showString == '2:':
        showStringRating = 2
        continue
    if showString == '1:':
        showStringRating = 1
        continue
    if showString == 'SPRINGSHOWSSTARTHERE':
        print('Changing to Spring')
        currentSeason = 'Spring'
        continue
    if showString == 'SUMMERSHOWSSTARTHERE':
        currentSeason = 'Summer'
        continue
    if showString == 'FALLSHOWSSTARTHERE':
        currentSeason = 'Fall'
        continue
    show.Name = showString
    show.Desc = "To Do"
    show.Rating = int(showStringRating)
    show.EndDate = "To Do"
    if currentSeason == 'Winter':
        seasons.addShowToWinter(show.__dict__)
    if currentSeason == 'Spring':
        seasons.addShowToSpring(show.__dict__)
    if currentSeason == 'Summer':
        seasons.addShowToSummer(show.__dict__)
    if currentSeason == 'Fall':
        seasons.addShowToFall(show.__dict__)
 
with open("AnimeDatabase.json", "w+") as text_file:
    text_file.write(json.dumps(seasons.__dict__))
        