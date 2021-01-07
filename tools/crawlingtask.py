from core.models.data_source_format_master import DataSourceFormatMaster
import time
import pandas as pd
from core.models.crawling_t_action_master import V4CrawlingTaskActionMaster
import json
from core import query_path


class WhenExist():
    SKIP = "skip"
    REPLACE = "replace"
    KEEP_BOTH = "keep both"


class sheet_type:
    MP3_SHEET_NAME = {"sheet_name": "MP_3", "fomatid": DataSourceFormatMaster.FORMAT_ID_MP3_FULL,
                      "column_name": ["track_id", "Memo", "Mp3_link", "url_to_add"]}
    MP4_SHEET_NAME = {"sheet_name": "MP_4", "fomatid": DataSourceFormatMaster.FORMAT_ID_MP4_FULL,
                      "column_name": ["track_id", "Memo", "MP4_link", "url_to_add"]}
    VERSION_SHEET_NAME = {"sheet_name": "Version_done", "fomatid": [DataSourceFormatMaster.FORMAT_ID_MP4_REMIX,
                                                                    DataSourceFormatMaster.FORMAT_ID_MP4_LIVE],
                          "column_name": ["track_id", "Remix_url", "Remix_artist", "Live_url", "Live_venue",
                                          "Live_year"]}


def crawl_itunes_album(ituneid: str, pic: str = "Joy_xinh", region: str = "us"):
    crawl_itunes_album = f"insert into crawlingtasks(Id, ActionId, TaskDetail, Priority) values (uuid4(), {V4CrawlingTaskActionMaster.ITUNES_ALBUM}, JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.album_id', '{ituneid}', '$.region', '{region}', '$.PIC', '{pic}'), 999);\n"
    return crawl_itunes_album


def crawl_youtube(track_id: str, youtube_url: str, format_id: str, when_exist: str = WhenExist.SKIP, place: str = None,
                  year: str = None, artist_cover: str = None,
                  pic: str = "Joy_xinh",
                  actionid: str = f"{V4CrawlingTaskActionMaster.DOWNLOAD_VIDEO_YOUTUBE}", priority: int = 1999):
    if artist_cover is not None:
        artist_cover = artist_cover.replace('\'', '\\\'').replace("\"", "\\\"")
    if place is not None:
        place = place.replace('\'', '\\\'').replace("\"", "\\\"")

    if format_id in (DataSourceFormatMaster.FORMAT_ID_MP4_FULL, DataSourceFormatMaster.FORMAT_ID_MP3_FULL,
                     DataSourceFormatMaster.FORMAT_ID_MP4_STATIC, DataSourceFormatMaster.FORMAT_ID_MP4_LYRIC):
        crawlingtask = f"insert into crawlingtasks(Id, ObjectID, ActionId, TaskDetail, Priority) values (uuid4(), '{track_id}', '{actionid}', JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.when_exists', '{when_exist}', '$.youtube_url', '{youtube_url}', '$.data_source_format_id', '{format_id}', '$.PIC', '{pic}'),{priority});\n"
    elif format_id in (DataSourceFormatMaster.FORMAT_ID_MP4_LIVE, DataSourceFormatMaster.FORMAT_ID_MP4_FAN_CAM):
        if place is None and year is None:
            crawlingtask = "-- missing info ---- concert_live_name or year"
        else:
            crawlingtask = f"insert into crawlingtasks(Id, ObjectID, ActionId, TaskDetail, Priority) values (uuid4(), '{track_id}', '{actionid}', JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.when_exists', '{when_exist}', '$.youtube_url', '{youtube_url}', '$.data_source_format_id', '{format_id}', '$.concert_live_name', '{place}','$.year', '{year}', '$.PIC', '{pic}'), {priority});\n"
    elif format_id == DataSourceFormatMaster.FORMAT_ID_MP4_COVER:
        if artist_cover is None:
            crawlingtask = "-- missing info ---- artist_cover"
        else:
            crawlingtask = f"insert into crawlingtasks(Id, ObjectID, ActionId, TaskDetail, Priority) values (uuid4(), '{track_id}', '{actionid}', JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.when_exists', '{when_exist}', '$.youtube_url', '{youtube_url}', '$.data_source_format_id', '{format_id}', '$.covered_artist_name', '{artist_cover}','$.year', '{year}', '$.PIC', '{pic}'), {priority});\n"
    else:
        crawlingtask = f"--formatid not support; \n"
    return crawlingtask


def convert_dict(raw_dict: dict):
    keys_values = raw_dict.items()
    result = ""
    for key, value in keys_values:
        result = result + f"{key}: '{value}', "
    result = "{" + result[:-2] + "}"
    print(result)
    # joy = {'name': 'a testing track', 'uuid': '5946AB77C52C45F8AA4283C1CF9EF70A'}
    # convert_dict(joy)


if __name__ == "__main__":
    start_time = time.time()
    k = crawl_youtube(track_id='joy', youtube_url='joy', format_id=DataSourceFormatMaster.FORMAT_ID_MP4_FULL)
    print(k)
    pd.set_option("display.max_rows", None, "display.max_columns", 50, 'display.width', 1000)
