from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, union, distinct, desc
from core.database_connection.sqlalchemy_create_engine import SQLALCHEMY_DATABASE_URI
from core.crud.sqlalchemy import get_compiled_raw_mysql

from core.models.datasource import DataSource
from core.models.playlist_datasource import PlaylistDataSource
from core.models.usernarrative import UserNarrative
from core.models.collection_datasource import CollectionDataSource

from typing import Optional, Tuple, Dict, List
from itertools import chain

from core.crud.get_df_from_query import get_df_from_query
import pandas as pd

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# def get_all_by_ids(data_source_id: list[str]) -> list[DataSource]:
#     return db_session.query(DataSource).filter((DataSource.id.in_(data_source_id)) & (DataSource.valid == 1)).all()


def get_datasourceid_from_youtube_url_and_trackid(youtube_url: str, trackid: str, formatid: str):
    datasourceid = (db_session.query(DataSource.id)
                    .select_from(DataSource)
                    .filter(DataSource.valid == 1,
                            DataSource.track_id == trackid,
                            DataSource.source_uri == youtube_url,
                            DataSource.format_id == formatid
                            )
                    )
    return datasourceid


def related_datasourceid(datasourceid: str):
    # Checking if exist in related_table
    datasourceid = (db_session.query(DataSource.id.label('datasourceid'), PlaylistDataSource.playlist_id,
                                     UserNarrative.id.label('narrative_id'),
                                     CollectionDataSource.collection_uuid)
                    .select_from(DataSource)
                    .outerjoin(PlaylistDataSource,
                               PlaylistDataSource.datasource_id == DataSource.id)
                    .outerjoin(UserNarrative,
                               UserNarrative.content_json.like("%" + DataSource.id + "%"))
                    .outerjoin(CollectionDataSource,
                               CollectionDataSource.datasource_id == DataSource.id)
                    .filter(DataSource.id == datasourceid)
                    )
    return datasourceid


def get_all_datasource_valid() -> List[DataSource]:
    return db_session.query(DataSource).filter((DataSource.valid == 1),
                                               DataSource.format_id == '74BA994CF2B54C40946EA62C3979DDA3').order_by(
        DataSource.created_at.desc()).all()


def get_all_by_ids(datasourceids: list):
    return db_session.query(DataSource).filter((DataSource.valid == 1),
                                               DataSource.id.in_(datasourceids)).order_by(
        DataSource.created_at.desc()).all()


if __name__ == "__main__":
    # pd.set_option("display.max_rows", None, "display.max_columns", 60, 'display.width', 1000)
    # datasourceids = ["BD399512B1B04EE28DBDB93D892081EB"]
    # db_datasources = get_all_by_ids(datasourceids)
    # for db_datasource in db_datasources:
    #     print(db_datasource.id)
    #     print(db_datasource.ext)


    pd.set_option("display.max_rows", None, "display.max_columns", 30, 'display.width', 1000)
    datasourceids = get_datasourceid_from_youtube_url_and_trackid('https://www.youtube.com/watch?v=xZUu3Q-YToE','BF1F3817A3B6458586991A7C80308299').all()
    datasourceids_flatten_list = tuple(set(list(chain.from_iterable(datasourceids))))  # flatten list
    print(datasourceids)
#
# related_id_datasource = related_datasourceid(datasourceids).all()
# flatten_list = list(set(list(chain.from_iterable(related_id_datasource))))   # flatten list
# flatten_list_remove_none = list(filter(lambda x: x is not None, flatten_list))
# if len(flatten_list_remove_none) == 0: #     Not exist in related table
#
#     print(len(flatten_list_remove_none))


# k = get_df_from_query(joy_xinh).values.flatten().tolist()
