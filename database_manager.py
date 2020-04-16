from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

title_genres = Table('title_genres', Base.metadata,
    Column('anime_id', Integer, ForeignKey('anime_list.anime_id')),
    Column('genre_id', Integer, ForeignKey('genre_list.genre_id'))
)

title_studios = Table('title_studios', Base.metadata,
    Column('anime_id', Integer, ForeignKey('anime_list.anime_id')),
    Column('studio_id', Integer, ForeignKey('studio_list.studio_id'))
)

title_licensors = Table('title_licensors', Base.metadata,
    Column('anime_id', Integer, ForeignKey('anime_list.anime_id')),
    Column('studio_id', Integer, ForeignKey('studio_list.studio_id'))
)

title_producers = Table('title_producers', Base.metadata,
    Column('anime_id', Integer, ForeignKey('anime_list.anime_id')),
    Column('studio_id', Integer, ForeignKey('studio_list.studio_id'))
)

class Anime(Base):
    __tablename__ = 'anime_list'
    anime_id = Column(Integer, primary_key = True)
    name = Column(String(20))
    link = Column(String(200))
    show_type = Column(String(20))
    number_of_episodes = Column(Integer)
    status = Column(String(100))
    season = Column(String(20))
    year = Column(Integer)
    producers = relationship('Studio', lambda: title_producers, backref = 'titles_producers')
    licensors = relationship('Studio', lambda: title_licensors, backref = 'titles_licensors')
    studios = relationship('Studio', lambda: title_studios, backref = 'titles_studios')
    source = Column(String(100))
    genres = relationship('Genre', lambda: title_genres, backref = 'titles_genres')
    duration = Column(Integer)
    age_rating = Column(String(20))
    score = Column(Float)
    rank = Column(Integer)
    popularity_rate = Column(Integer)
    members = Column(Integer)
    favorites = Column(Integer)


class Genre(Base):
    __tablename__ = 'genre_list'
    genre_id = Column(Integer, primary_key = True)
    genre_name = Column(String(100))

class Studio(Base):
    __tablename__ = 'studio_list'
    studio_id = Column(Integer, primary_key = True)
    studio_name = Column(String(200))

engine = create_engine('sqlite:///animelist.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class DataManager():
    def __init__(self, genres_list, studios_list):
        session = Session()

        for genre in genres_list :
            session.add(Genre(genre_name = genre))

        for studio in studios_list :
            session.add(Studio(studio_name = studio))

        session.commit()
        self.genre_list = self.get_all(Genre)
        self.studio_list = self.get_all(Studio)
        session.close()

    def add_anime(self, anime):
        session = Session()
        anime_obj = Anime(
            anime_id = anime['id'],
            name = anime['name'],
            link = anime['link'],
            show_type = anime['type'],
            number_of_episodes = anime['number_of_episodes'],
            status = anime['status'],
            season = anime['season'],
            year = anime['year'],
            source = anime['source'],
            duration = anime['duration'],
            age_rating = anime['age_rating'],
            score = anime['score'],
            rank = anime['rank'],
            popularity_rate = anime['popularity_rate'],
            members = anime['members'],
            favorites = anime['favorites']
        )
        
        for genre in anime['genres']:
            anime_obj.genres.append(self.get_genre(genre))

        for studio in anime['studios']:
            anime_obj.studios.append(self.get_studio(studio))

        for licensor in anime['licensors']:
            anime_obj.licensors.append(self.get_studio(licensor))

        for producer in anime['producers']:
            anime_obj.producers.append(self.get_studio(producer))

        session.add(anime_obj)
        session.commit()
        session.close()

    def get_all(self, table_class):
        session = Session()
        query = session.query(table_class).all()
        session.close()

        entries = {
            'dicts' : [],
            'objects' : []
        }

        for row in query:
            entries['dicts'].append(row.__dict__)
            entries['objects'].append(row)

        return entries

    def get_genre(self, genre_name):
        for genre in self.genre_list['dicts'] :
            if genre['genre_name'] == genre_name :
                return self.genre_list['objects'][int(genre['genre_id']) - 1]

    def get_studio(self, studio_name):
        for studio in self.studio_list['dicts'] :
            if studio['studio_name'] == studio_name :
                return self.studio_list['objects'][int(studio['studio_id']) - 1]
        # return session.query(Studio).filter(Studio.studio_name == 'sunrise').first()





