#Step one, fetch https://myanimelist.net/anime/season/<year>/<season>
#Step two, compile all the listed anime into name and hyperlink.
#tags are <div class="seasonal-anime js-seasonal-anime" .... </div>
#tags contain Name, Hyperlink between <a href and \n. Get second instance in regex
#Parse out link from a href=" to first " without including "
#Parse out name by striping from first > to first <
#Go to hyperlink, look for >Aired:</span>
#Get from poistion to first </div> after
#If string has ? not finished airing. Add name to blacklist, incase this title goes into other seasons.

import requests
import re
from re import RegexFlag
import time

season = 'spring'
year = '2018'
url = 'https://myanimelist.net/anime/season/'+year+'/'+season


response = requests.get(url)
taggedList = re.findall('<div class=\"seasonal-anime js-seasonal-anime\".*?</div>', str(response.content))
for tag in taggedList:
    time.sleep(5)
    AnimeName = re.findall('link-title\">.*?</a>', tag)[0].replace('link-title">','').replace('</a>', '')
    AnimeUrl = re.findall('<a href=".*? ', tag)[0].replace('<a href="','').replace('/video"','')
    response = str(requests.get(AnimeUrl).content)
    Aired = re.findall('<span class="dark_text">Aired:</span>.*?</div>',response)[0].replace('\\n','').replace('<span class="dark_text">Aired:</span>','').replace('</div>','')[1:-1]
    if('Currently Airing' in response):
        print(AnimeName+' Is still airing. ('+Aired+')')
    else:
         print(AnimeName+' Has finished airing.('+Aired+')')
