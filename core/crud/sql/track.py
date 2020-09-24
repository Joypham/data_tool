from core.models.track import Track
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, union, distinct, desc
from core.database_connection.sqlalchemy_create_engine import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_track_wiki(trackid: tuple):
    track_wiki = (db_session.query(Track.id,
                                   Track.title,
                                   Track.artist,
                                   func.json_extract(Track.info, "$.wiki_url").label("wiki_url"),
                                   func.json_extract(Track.info, "$.wiki.brief").label("wiki_content")
                                   )
                  .select_from(Track)
                  .filter(Track.id.in_(trackid))
                  )
    return track_wiki


def get_track_lyric(trackid: tuple):
    track_lyrics = (db_session.query(Track.id,
                                     Track.title,
                                     Track.artist,
                                     Track.lyrics
                                     )
                    .select_from(Track)
                    .filter(Track.id.in_(trackid))
                    )
    return track_lyrics


# def test(trackid: str):
#     test = (db_session.query(Track.id,
#                              Track.title,
#                              Track.artist
#                              )
#             .select_from(Track)
#             .filter(Track.id == trackid)
#             )
#     return test
