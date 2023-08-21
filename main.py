import requests
from bs4 import BeautifulSoup
from translate import Translator

translator= Translator(from_lang='ru',to_lang='en') #set up a translator

game = input("type game name: ") #to use in the search bar
search_data = {  #to make a post request in the search
    'do': 'search',
    'subaction': 'search',
    'story': game
}
r = requests.post("https://freetp.org/", data=search_data) #getting website with post request
soup = BeautifulSoup(r.text, 'html.parser')  #beautifulsoup 4 parser
games_names = soup.find(id="dle-content").findAll(class_="base") #get the result of the search into a list
games_names.remove(games_names[0]) #remove the first item on the list due to it being always not part of the search result
r_gamelist = [requests.get(name.a.get('href')) for name in games_names] #make a list for gotten websutes of the games in the search result
gamelist = [BeautifulSoup(request.text, 'html.parser') for request in r_gamelist] #make a list of beautifulsoup 4 parsered of game websites
for game,name in zip(gamelist,games_names): #scroll through games and their names in order to analyze and show
    tutorial = game.find(class_="base fullstory").findAll('p') #get all the game description
    print(translator.translate(name.a.get_text())) #translate the name of the game and show it
    try: #remove the first part of the description and if it was a trailer and gave an error then skip the game
        tutorial.remove(tutorial[0])
        tutorial.remove(tutorial[0])
        tutorial.remove(tutorial[0])
        tutorial.remove(tutorial[0])
    except:
        continue
    for step in tutorial: #scroll through the description
        print(translator.translate(str(step.get_text()))) #print the text
        print("https:"+step.find('a').get('href')) if step.find(class_="attachment") in step or step.find('a') in step else None #print the links
    print("\n\n////////////////////////\n\n") #to make it easier to identify the text of each game