import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import sqlite3
from database_manager import DataManager

def genre_scraper():
    page = requests.get('https://myanimelist.net/anime.php')
    genres_list = []
    if page.status_code is 200 :
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.select('div.anime-manga-search > div:nth-child(2) > div > div > a')
        for link in results :
            genres_list.append(link.text.split(' (')[0].lower().strip())

    return genres_list

def studios_scraper():
    page = requests.get('https://myanimelist.net/anime/producer')
    studios_list = []
    if page.status_code is 200 :
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.select('.genre-name-link')
        for link in results :
            studios_list.append(link.text.split(' (')[0].lower().strip())

    return studios_list


# def all_anime():
#     start_date = datetime.now().date()
#     conn = sqlite3.connect(f'animelist-{start_date}.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE ANIME_LIST
#                 (ID int, NAME text, LINK text)''')
#     conn.commit()

#     counter = 0

#     while True :
#         url = f'https://myanimelist.net/topanime.php?limit={counter*50}'

#         page = requests.get(url)

#         if page.status_code is 200 :

#             soup = BeautifulSoup(page.content, 'html.parser')

#             results = soup.select('tr > td > div > div > a.hoverinfo_trigger')

#             for link in results:
#                 anime = {
#                     'ID' : int(re.findall(r'\d+', link['href'])[0]),
#                     'NAME' : link.text,
#                     'LINK' : link['href']
#                 }
                
#                 c.execute("INSERT INTO ANIME_LIST VALUES (?, ?, ?)", [anime["ID"], anime["NAME"], anime["LINK"]])
            
#             conn.commit()

#             print(counter*50)
#             counter += 1
        
#         else :
#             break

        
#     conn.close()



def populate_database(genre_list):
    conn = sqlite3.connect(f'animelist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE genres
                (
                    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    genre TEXT
                )'''
            )

    c.execute('''CREATE TABLE anime_list
                (
                    anime_id INTEGER PRIMARY KEY, 
                    name TEXT, link TEXT, 
                    score REAL, 
                    status TEXT, 
                    season TEXT, 
                    source TEXT, 
                    age_rating TEXT, 
                    type TEXT
                )'''
            )
    
    c.execute('''CREATE TABLE anime_genre
                (
                    anime_genre_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    anime INTEGER,  
                    genre INTEGER,
                    FOREIGN KEY (anime)  REFERENCES anime_list(anime_id),
                    FOREIGN KEY (genre)  REFERENCES genres(genre_id)
                )'''
            )

   
    for genre in genre_list :
        c.execute('''INSERT INTO genres (genre)
                VALUES(?)''', [genre])
    conn.commit()
    conn.close()

# duration is in minutes
cowboy_bebop = {
    'id' : 1,
    'name' : 'Cowboy Bebop',
    'link' : 'https://myanimelist.net/anime/1/Cowboy_Bebop',
    'type' : 'tv',
    'number_of_episodes' : 26,
    'status' : 'finished airing',
    'season' : 'spring 1998',
    'year' : 1998,
    'producers' : [ 'bandai visual' ],
    'licensors' : [ 'funimation', 'bandai visual' ],
    'studios' : [ 'sunrise' ],
    'source' : 'original',
    'genres' : [ 'action', 'adventure', 'comedy', 'drama', 'sci-fi', 'space' ],
    'duration' : 24,
    'age_rating' : 'R-17+',
    'score' : 8.79,
    'rank' : 28,
    'popularity_rate' : 39,
    'members' : 982561,
    'favorites' : 51401
} 

genres_list = genre_scraper()
studios_list = studios_scraper()
# populate_database(genres_list)
dm = DataManager(genres_list, studios_list)
dm.add_anime(cowboy_bebop)