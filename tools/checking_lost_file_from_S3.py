from core.aws.aws_config import AWSConfig
from core.aws.s3.aws_s3 import existing_on_s3
from core.crud.sql.datasource import get_all_by_ids
from google_spreadsheet_api.function import get_df_from_speadsheet, get_gsheet_name
from core.models.data_source_format_master import DataSourceFormatMaster
from core import query_path



def checking_lost_datasource_from_S3(datasource_ids: list):
    print("start")
    db_datasources = get_all_by_ids(datasource_ids)

    for db_datasource in db_datasources:
        if "berserker" in db_datasource.cdn:
            key = f"videos/{db_datasource.file_name}"
        else:
            key = f"audio/{db_datasource.file_name}"
        result = existing_on_s3(key)
        print(f"{key}---{AWSConfig.S3_DEFAULT_BUCKET}")
        print(f"Datasource id: [{db_datasource.id}] - {result}")
        with open(query_path, "a+") as f:
            if result == 0 and db_datasource.format_id in (
                    DataSourceFormatMaster.FORMAT_ID_MP3_FULL, DataSourceFormatMaster.FORMAT_ID_MP4_FULL):
                joy_xinh = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values (uuid4(),'{db_datasource.track_id}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','replace' ,'$.youtube_url','{db_datasource.source_uri}','$.data_source_format_id','{db_datasource.format_id}','$.PIC', '{gsheet_name}_{sheet_name}'),1999);\n"
                print(joy_xinh)
                f.write(joy_xinh)
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
    # https://docs.google.com/spreadsheets/d/1GjK710m_23jBT4xVe21IN_FbNkxDk-CVzHwHWVLaIRA/edit#gid=1490664877
    gsheetid = '1GjK710m_23jBT4xVe21IN_FbNkxDk-CVzHwHWVLaIRA'
    gsheet_name = get_gsheet_name(gsheet_id=gsheetid)
    sheet_name = 'DatasourceID'
    df = get_df_from_speadsheet(gsheet_id=gsheetid, sheet_name=sheet_name)
    df = df.head(10)
    list_dsid = df['id'].values.tolist()
    checking_lost_datasource_from_S3(list_dsid)
