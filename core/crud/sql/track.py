from core.models.track import Track
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, union, distinct, desc
from core.database_connection.sqlalchemy_create_engine import SQLALCHEMY_DATABASE_URI

from core.crud.sqlalchemy import get_compiled_raw_mysql

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


def get_all_by_track_ids(trackids: list):
    return db_session.query(Track).filter((Track.valid == 1),
                                          Track.id.in_(trackids)).order_by(
        Track.created_at.desc()).all()


# if __name__ == "__main__":
#     trackid = 'DE365F7B42C646199F372F6A24C42994'
#     db_tracks = get_all_by_track_id(trackid)
#     print(db_tracks.id)
    # for db_track in db_tracks:
    #     print(db_track.id)
    #     print(db_track.ext)

