from core.aws.aws_config import AWSConfig
from core.aws.s3.aws_s3 import existing_on_s3
from core.crud.sql.datasource import get_all_datasource_by_ids, get_one_datasource_by_id
from core.crud.sql.track import get_one_track_by_id

from google_spreadsheet_api.function import get_df_from_speadsheet, get_gsheet_name
from core.models.data_source_format_master import DataSourceFormatMaster
from core import query_path
from tools.crawlingtask import crawl_youtube, WhenExist
import pandas as pd
import time

import inspect


def get_split_info(vibbidi_title: str, track_title: str):
    k = vibbidi_title.replace(track_title, "").strip()[1:-1]
    raw_year = k.split(' ')[-1]
    if raw_year.isnumeric():
        year = raw_year
        concert_live_name = k.replace(year, "")
    else:
        year = ''
        concert_live_name = k
    return {"year": year, "concert_live_name": concert_live_name}


def checking_lost_datasource_from_S3(datasource_id: str):
    db_datasource = get_one_datasource_by_id(datasource_id)

    if "berserker" in db_datasource.cdn:
        key = f"videos/{db_datasource.file_name}"
    else:
        key = f"audio/{db_datasource.file_name}"
    result = existing_on_s3(key)
    print(f"{key}---{AWSConfig.S3_DEFAULT_BUCKET}")
    print(f"Datasource id: [{db_datasource.id}] - {result}")
    return result


def proccess_file_name_lost_from_S3(datasource_ids: list):
    print("start checking_lost_datasource_from_S3")
    db_datasources = get_all_datasource_by_ids(datasource_ids)
    for db_datasource in db_datasources:
        # step 1: check lost file from datasourceid
        if "berserker" in db_datasource.cdn:
            key = f"videos/{db_datasource.file_name}"
        else:
            key = f"audio/{db_datasource.file_name}"
        result = existing_on_s3(key)
        print(f"{key}---{AWSConfig.S3_DEFAULT_BUCKET}")
        print(f"Datasource id: [{db_datasource.id}] - {result}")

        # Step 2: get datasource lost from S3
        if result == 0:
            with open('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/datasource_id', "a+") as f1:
                if db_datasource.track_id == '':
                    joy_xinh_qua = f"datasource not have trackid-------{db_datasource.id}-------{db_datasource.format_id}-------{db_datasource.source_uri};\n"
                    f1.write(joy_xinh_qua)
                else:
                    db_track = get_one_track_by_id(db_datasource.track_id)
                    if not db_track:
                        joy_xinh_qua = f"not existed track_valid-------{db_datasource.id}-------{db_datasource.format_id}-------{db_datasource.source_uri};\n"
                        f1.write(joy_xinh_qua)
                    else:
                        joy_xinh_qua = f"{db_track.id}-------{db_datasource.id}-------{db_datasource.format_id}-------{db_datasource.source_uri};\n"
                        f1.write(joy_xinh_qua)

                        # Step 3: to fix datasource lost from S3
                        with open(query_path, "a+") as f2:
                            if db_datasource.format_id in (
                                    DataSourceFormatMaster.FORMAT_ID_MP3_FULL,
                                    DataSourceFormatMaster.FORMAT_ID_MP4_FULL,
                                    DataSourceFormatMaster.FORMAT_ID_MP4_STATIC,
                                    DataSourceFormatMaster.FORMAT_ID_MP4_LYRIC):
                                joy_xinh = crawl_youtube(track_id=db_track.id, youtube_url=db_datasource.source_uri,
                                                         format_id=db_datasource.format_id,
                                                         when_exist=WhenExist.REPLACE,
                                                         pic=f"{gsheet_name}_{sheet_name}", priority=1999)
                                f2.write(joy_xinh)
                            elif result == 0 and db_datasource.format_id == DataSourceFormatMaster.FORMAT_ID_MP4_LIVE:
                                vibbidi_title = db_datasource.info.get('vibbidi_title')
                                track_title = db_track.title
                                live_info = get_split_info(vibbidi_title=vibbidi_title, track_title=track_title)
                                joy_xinh = crawl_youtube(track_id=db_track.id, youtube_url=db_datasource.source_uri,
                                                         format_id=db_datasource.format_id,
                                                         when_exist=WhenExist.REPLACE,
                                                         place=live_info.get('concert_live_name'),
                                                         year=live_info.get('year'),
                                                         pic=f"{gsheet_name}_{sheet_name}",
                                                         priority=1999)
                                f2.write(joy_xinh)
                            else:
                                continue


def checking_lost_datasource_resize_image_from_S3(db_datasource: object):
    method_name = inspect.stack()[0][3]
    ext_keys = db_datasource.ext.keys()
    expect_resize_image_types = ["micro", "tiny", "small", "medium", "large", "extra"]
    result = ""
    with open(query_path, "a+") as f:
        if "resize_images" in ext_keys:
            for expect_resize_image_type in expect_resize_image_types:
                actual_resize_images = db_datasource.ext.get('resize_images')
                loop = False
                joy_xinh = ""
                for existed_resize_image in actual_resize_images:
                    existed_resize_image_type = existed_resize_image.split(".")[-2]
                    if existed_resize_image_type == expect_resize_image_type:
                        loop = True
                        if "video" in existed_resize_image:
                            key = f"videos/{existed_resize_image}"
                        else:
                            key = f"audio/{existed_resize_image}"
                        checking_exist_file_on_S3 = existing_on_s3(key, bucket=AWSConfig.S3_DEFAULT_BUCKET)
                        joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, {expect_resize_image_type}, {checking_exist_file_on_S3}, {key}, {db_datasource.source_uri}\n"
                        if not checking_exist_file_on_S3:
                            f.write(joy_xinh)
                        break
                    else:
                        continue
                result = result + joy_xinh
                if not loop:
                    joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, {expect_resize_image_type}, not have, not have, not have\n"
                    result = result + f"{method_name}, {db_datasource.id}, {expect_resize_image_type}, not have, not have, not have\n"
                    f.write(joy_xinh)
        else:
            result = result + f"{method_name}, {db_datasource.id}, not have, not have, not have, not have\n"
            joy_xinh = f"{method_name}, {db_datasource.id}, not have, not have, not have, not have\n"
            f.write(joy_xinh)
        print(result)


def checking_lost_datasource_default_image_from_S3(db_datasource: object):
    method_name = inspect.stack()[0][3]
    with open(query_path, "a+") as f:
        if "berserker" in db_datasource.cdn:
            key = f"videos/{db_datasource.file_name}.jpg"
        else:
            key = f"audio/{db_datasource.file_name}.jpg"
        result = existing_on_s3(s3_key=key, bucket=AWSConfig.S3_DEFAULT_BUCKET)
        print(f"{method_name}, {key}---{AWSConfig.S3_DEFAULT_BUCKET}----{result}")
        if not result:
            joy_xinh = f"{method_name}, {db_datasource.id}, None, {result}, {key}, {db_datasource.source_uri}\n"
            f.write(joy_xinh)


def checking_lost_datasource_background_from_S3(db_datasource):
    method_name = inspect.stack()[0][3]
    with open(query_path, "a+") as f:
        datasource_ext_key = db_datasource.ext.keys()
        expect_background_types = ["bg_360_file_name", "bg_720_file_name"]
        if db_datasource.format_id in (
        DataSourceFormatMaster.FORMAT_ID_MP4_FULL, DataSourceFormatMaster.FORMAT_ID_MP4_LIVE):
            for expect_background_type in expect_background_types:
                joy_xinh = ""
                if expect_background_type in datasource_ext_key:
                    bg_file_name_key = f"videos/{db_datasource.ext[expect_background_type]}"
                    result_bg_file_name = existing_on_s3(bg_file_name_key)
                    print(f"{expect_background_type}----{result_bg_file_name}----{bg_file_name_key}")
                    if not result_bg_file_name:
                        joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, {expect_background_type}, {result_bg_file_name}, {bg_file_name_key}, {db_datasource.source_uri}\n"
                else:
                    print(f"{expect_background_type}----not have----not have")
                    joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, {expect_background_type}, not have, not have, {db_datasource.source_uri}\n"
                print(joy_xinh)
                f.write(joy_xinh)


def checking_lost_static_video_from_S3(db_datasource):
    method_name = inspect.stack()[0][3]
    with open(query_path, "a+") as f:
        if db_datasource.format_id == DataSourceFormatMaster.FORMAT_ID_MP3_FULL:
            joy_xinh = ""
            datasource_ext_key = db_datasource.ext.keys()
            if 'static_video' in datasource_ext_key:
                if 'file_name' in db_datasource.ext['static_video'].keys():
                    key = f"videos/{db_datasource.ext['static_video']['file_name']}"
                    result = existing_on_s3(key)
                    print(f"{method_name}, {key}---{AWSConfig.S3_DEFAULT_BUCKET}----{result}")
                    if not result:
                        joy_xinh = f"{method_name}, {db_datasource.id}, None, {result}, {key}, {db_datasource.source_uri}\n"
                else:
                    joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, None, not have, not have, {db_datasource.source_uri}\n"
            else:
                joy_xinh = joy_xinh + f"{method_name}, {db_datasource.id}, None, not have, not have, {db_datasource.source_uri}\n"
            print(joy_xinh)
            f.write(joy_xinh)


if __name__ == "__main__":
    # https://docs.google.com/spreadsheets/d/1Qu5oUocflDr4ERJvux8eSnuVVIGp1-WNzjqE7NeYKJI/edit#gid=709402142

    start_time = time.time()
    # gsheetid = '1Qu5oUocflDr4ERJvux8eSnuVVIGp1-WNzjqE7NeYKJI'
    # gsheet_name = get_gsheet_name(gsheet_id=gsheetid)
    # sheet_name = 'checking lost resize image from S3'
    # df = get_df_from_speadsheet(gsheet_id=gsheetid, sheet_name=sheet_name)
    # list_dsid = list(dict.fromkeys(df['datasourceid'].values.tolist()))
    list_dsid = [
        "85562061DC794C7082A80838ECD00C21",
        "F3ED1BFEB02E451188351CF0802429E7",
        "2D578249F2C949F6AE0AA9AB20159804",
        "B197B967140C4E22ABD7D6588F82BD14",
        "D50B2CE3245740349418B4D1653F78A0",
        "C8DCD912FCAE438483B4C0A610E1FC7F",
        "8BA6954BE35E41D594F236B26038C895",
        "A900806FAA754F5792CFB927D303CF53"
    ]
    for dsid in list_dsid:
        print(dsid + "\n")
        db_datasource = get_one_datasource_by_id(dsid)
        # checking_lost_datasource_resize_image_from_S3(db_datasource=db_datasource)
        # checking_lost_datasource_default_image_from_S3(db_datasource=db_datasource)
        # checking_lost_datasource_background_from_S3(db_datasource)
        checking_lost_static_video_from_S3(db_datasource)
    # proccess_file_name_lost_from_S3(list_dsid)
    # list_dsid = [
    #     "F3ED1BFEB02E451188351CF0802429E7",
    #     "2D578249F2C949F6AE0AA9AB20159804",
    #     "B197B967140C4E22ABD7D6588F82BD14",
    #     "D50B2CE3245740349418B4D1653F78A0",
    #     "C8DCD912FCAE438483B4C0A610E1FC7F"
    # ]
    print("\n --- %s seconds ---" % (time.time() - start_time))
