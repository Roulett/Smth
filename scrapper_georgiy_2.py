import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import pathlib
import os
import shutil
from google.colab import files

def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        print(source, destination, archive_from, archive_to)
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

def search_(word, game,search_engine,game_english):
  if search_engine == 'google':
    URL = "https://www.google.com/search?q={}+{}&tbm=isch&ved=2ahUKEwi445H0sM_1AhXICHcKHdX1C2kQ2-cCegQIABAA&oq=carcassonne+board&gs_lcp=CgNpbWcQAzIECAAQQzIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIGCAAQBRAeMgYIABAIEB4yBggAEAgQHjoGCAAQBxAeUOkIWOkIYLwKaABwAHgAgAFmiAHLAZIBAzAuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=sDnxYbjLGsiR3APV66_IBg&bih=854&biw=1496&client=safari".format(game,word)
  elif search_engine == 'yandex':
    URL = "https://yandex.ru/images/search?text={}%20{}&from=tabbar".format(game,word)
  elif search_engine == 'bing':
    URL = "https://www.bing.com/images/search?q={}+{}&form=AWIR&first=1&tsc=ImageBasicHover".format(game,word)
  elif search_engine == 'DuckDuckGo':
    URL = "https://duckduckgo.com/?q={}+{}&t=h_&iax=images&ia=images".format(game,word)
  CURRENT_CLASS = game_english

  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'}
  page = requests.get(URL, headers=headers)

  soup = BeautifulSoup(page.content, "html.parser")
  images_links = re.findall(r'http[^"]+.(?:png|jpeg|jpg)', str(soup))

  print('Founded', len(images_links), 'new images')
  try:
    os.mkdir(game_english)
  except FileExistsError:
    pass
  files_count = len([s for s in os.listdir(CURRENT_CLASS) if os.path.isfile(os.path.join(CURRENT_CLASS, s))])
  for index, image_link in enumerate(images_links):
    for ext in ['.png', '.jpeg', '.jpg']:
        if ext in image_link:
            try:
                urlretrieve(image_link, os.path.join(CURRENT_CLASS, CURRENT_CLASS + '_' + str(files_count + index) + ext))
            except:
              pass

list_words_english = ['game','board','set', 'play', 'mattel']
list_words_russian = ['игра', 'играть', 'доска', 'купить','настольная', 'настолка']
list_words_french = ['jeu','jouer']
list_words_german = ['spiel','spielen', 'aufstellung', 'kaufen','brettspiele']
list_words_spanish = ['juego', 'de+mesa', 'jugar', 'comprar']
list_full = list_words_english + list_words_spanish + list_words_german + list_words_french + list_words_russian
search_engines = ['bing']#, 'yandex', , 'DuckDuckGo']'bing','google'
list_games = [{'en': 'qwirkle', 'de': 'qwirkle', 'ru': 'qwirkle', 'es': 'qwirkle', 'fr' :'qwirkle'},{'en': 'qwirkle', 'de': 'qwirkle', 'ru': 'qwirkle', 'es': 'qwirkle', 'fr' :'qwirkle'},
              {'en': 'mastermind', 'de': 'mastermind', 'ru': 'мастермайнд', 'es': 'mastermind', 'fr' :'mastermind'},
              {'en': 'agricola', 'de': 'agricola', 'ru': 'agricola', 'es': 'agricola', 'fr' :'agricola'},
              {'en': 'axis+and+allies', 'de': 'axis+and+allies', 'ru': 'axis+and+allies', 'es': 'axis+and+allies', 'fr' :'axis+and+allies'},
              {'en': 'jenga', 'de': 'jenga', 'ru': 'дженга', 'es': 'jenga', 'fr' :'jenga'},
              {'en': 'risk', 'de': 'risiko', 'ru': 'риск', 'es': 'risk', 'fr' :'risk'},
              {'en': 'stratego', 'de': 'stratego', 'ru': 'стратего', 'es': 'stratego', 'fr' :'stratego'},
              {'en': 'mancala', 'de': 'mancala', 'ru': 'манкала', 'es': 'mancala', 'fr' :'mancala'},
              {'en': 'reversi', 'de': 'reversi', 'ru': 'реверси', 'es': 'reversi', 'fr' :'reversi'},
              {'en': 'rummikub', 'de': 'rummikub', 'ru': 'руммикуб', 'es': 'rummikub', 'fr' :'rummikub'}
              ]

for dict_base in list_games:
  dict_words_languages = {dict_base['de']: list_words_german,
                        dict_base['es']: list_words_spanish,
                        dict_base['fr']: list_words_french,
                        dict_base['ru']: list_words_russian,
                        dict_base['en']: list_full}
  for game_name,list_words in dict_words_languages.items():
    for list_word in list_words:
      for search_engine in search_engines:
        search_(list_word,game_name,search_engine,dict_base['en'])
  make_archive('/content/{}'.format(dict_base['en']), '/content/{}.zip'.format(dict_base['en']))