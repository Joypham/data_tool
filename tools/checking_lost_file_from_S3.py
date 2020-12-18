from core.aws.aws_config import AWSConfig
from core.aws.s3.aws_s3 import existing_on_s3
from core.crud.sql.datasource import get_all_by_ids
from core.crud.sql.track import get_one_by_id
from google_spreadsheet_api.function import get_df_from_speadsheet, get_gsheet_name
from core.models.data_source_format_master import DataSourceFormatMaster
from core import query_path
import time


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


def checking_lost_datasource_from_S3(datasource_ids: list):
    print("start")
    db_datasources = get_all_by_ids(datasource_ids)

    for db_datasource in db_datasources:
        trackid = db_datasource.track_id
        db_track = get_one_by_id(trackid)

        if "berserker" in db_datasource.cdn:
            key = f"videos/{db_datasource.file_name}"
        else:
            key = f"audio/{db_datasource.file_name}"
        result = existing_on_s3(key)
        print(f"{key}---{AWSConfig.S3_DEFAULT_BUCKET}")
        print(f"Datasource id: [{db_datasource.id}] - {result}")
        with open('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/datasource_id', "a+") as f1:
            if result == 0:
                joy_xinh_qua = f"{db_datasource.track_id} -------{db_datasource.id}-------{db_datasource.format_id};\n"
                f1.write(joy_xinh_qua)

        with open(query_path, "a+") as f2:
            if result == 0 and db_datasource.format_id in (
                    DataSourceFormatMaster.FORMAT_ID_MP3_FULL, DataSourceFormatMaster.FORMAT_ID_MP4_FULL, DataSourceFormatMaster.FORMAT_ID_MP4_STATIC):
                joy_xinh = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values (uuid4(),'{db_datasource.track_id}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','replace' ,'$.youtube_url','{db_datasource.source_uri}','$.data_source_format_id','{db_datasource.format_id}','$.PIC', '{gsheet_name}_{sheet_name}'),1999);\n"
                f2.write(joy_xinh)
            elif result == 0 and db_datasource.format_id == DataSourceFormatMaster.FORMAT_ID_MP4_LIVE:
                vibbidi_title = db_datasource.info.get('vibbidi_title')
                track_title = db_track.title
                live_info = get_split_info(vibbidi_title=vibbidi_title, track_title= track_title)
                joy_xinh = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values (uuid4(),'{db_datasource.track_id}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','keep both' ,'$.youtube_url','{db_datasource.source_uri}','$.data_source_format_id',{DataSourceFormatMaster.FORMAT_ID_MP4_LIVE},'$.concert_live_name','{live_info.get('concert_live_name')}','$.year','{live_info.get('year')}','$.PIC', '{gsheet_name}_{sheet_name}'),1999);\n"
                f2.write(joy_xinh)
            else:
                continue


        # print(existing_on_s3(key, bucket=AWSConfig.S3_IMAGE_BUCKET))


def checking_lost_datasource_image_from_S3(datasource_ids: list):
    print("start")
    db_datasources = get_all_by_ids(datasource_ids)
    resize_image_types = ["micro", "tiny", "small", "medium", "large", "extra"]

    for db_datasource in db_datasources:
        for resize_image_type in resize_image_types:
            resize_image_type = resize_image_type

            if db_datasource.is_video == 1:
                key = f"videos/{db_datasource.file_name}.{resize_image_type}.jpg"
                # print(key)

            else:
                key = f"audio/{db_datasource.file_name}.{resize_image_type}.jpg"
                # print(key)
            result = existing_on_s3(key, bucket=AWSConfig.S3_DEFAULT_BUCKET)
            print(f"Datasource id: [{db_datasource.id}] -[{resize_image_type}] - [{result}]")

        # print(existing_on_s3(key, bucket=AWSConfig.S3_IMAGE_BUCKET))


# def checking_lost_track_image_from_S3(trackid: list):


if __name__ == "__main__":
    # https://docs.google.com/spreadsheets/d/1xPh0ypmOz5AV4HYCNiaPLV533y2Gvfl_CX9tFa9tssU/edit#gid=1113758411
    start_time = time.time()
    gsheetid = '1xPh0ypmOz5AV4HYCNiaPLV533y2Gvfl_CX9tFa9tssU'
    gsheet_name = get_gsheet_name(gsheet_id=gsheetid)
    sheet_name = 'DatasourceID'
    df = get_df_from_speadsheet(gsheet_id=gsheetid, sheet_name=sheet_name)
    list_dsid = df['datasourceid'].values.tolist()
    # list_dsid = ["0E8F169898BA496A9749D2B34F828696", "143908C73F4B4864A84A50BB778EC5ED"]
    checking_lost_datasource_from_S3(list_dsid)

    print("\n --- %s seconds ---" % (time.time() - start_time))


