from core.aws.aws_config import AWSConfig
from core.aws.s3.aws_s3 import existing_on_s3
from core.crud.sql.datasource import get_all_by_ids, get_all_datasource_valid
from core.crud.sql.track import get_all_by_track_ids
from core.models.data_source_format_master import DataSourceFormatMaster
import json


def checking_lost_datasource_filename_from_S3(datasource_ids: list):
    print("start checking datasource filename")
    db_datasources = get_all_by_ids(datasource_ids)

    for db_datasource in db_datasources:
        if db_datasource.is_video == 1:
            key = f"videos/{db_datasource.file_name}"

        else:
            key = f"audio/{db_datasource.file_name}"
        result = existing_on_s3(key)
        print(f"filename: {db_datasource.file_name} - {result}", "\n")
        # print(existing_on_s3(key, bucket=AWSConfig.S3_IMAGE_BUCKET))


def checking_lost_datasource_image_from_S3(datasource_ids: list):
    print("start checking datasource image")
    db_datasources = get_all_by_ids(datasource_ids)
    for db_datasource in db_datasources:
        resize_images = db_datasource.ext.get('resize_images')
        for resize_image in resize_images:
            if db_datasource.is_video == 1:
                key = f"videos/{resize_image}"
            else:
                key = f"audio/{resize_image}"
            result = existing_on_s3(key, bucket=AWSConfig.S3_DEFAULT_BUCKET)
            print(
                f"filename: {key} - {result}")


def checking_lost_datasource_background_from_S3(datasource_ids: list):
    print("\nstart checking background")
    db_datasources = get_all_by_ids(datasource_ids)
    for db_datasource in db_datasources:
        if db_datasource.format_id in ("74BA994CF2B54C40946EA62C3979DDA3", "7F8B6CD82F28437888BD029EFDA1E57F"):
            try:
                bg_720_file_name = db_datasource.ext['bg_720_file_name']
                bg_360_file_name = db_datasource.ext['bg_360_file_name']
                key_720 = f"videos/{bg_720_file_name}"
                key_360 = f"videos/{bg_360_file_name}"
                result1 = existing_on_s3(key_720)
                result2 = existing_on_s3(key_360)
                print(f"filename: {bg_720_file_name} - {result1}")
                print(f"filename: {bg_360_file_name} - {result2}")
            except KeyError:
                print(f"Datasourceid: {db_datasource.id} not have background - False")

        else:
            print(f"formatid: {db_datasource.format_id} not required background - True")


def checking_lost_pip_from_S3(datasource_ids: list):
    print("\nstart checking pip")
    db_datasources = get_all_by_ids(datasource_ids)
    for db_datasource in db_datasources:
        print()
        if db_datasource.format_id == "1A67A5F1E0D84FB9B48234AE65086375":
            try:

                pip = db_datasource.ext['static_video']['file_name']
                key_pip = f"videos/{pip}"
                result = existing_on_s3(key_pip)
                print(f"filename: {key_pip} - {result}")

                trackid = [db_datasource.track_id]
                db_trackids = get_all_by_track_ids(trackid)
                for db_trackid in db_trackids:
                    if db_trackid.image_url == db_datasource.ext['static_video']['image_url']:
                        print(f"datasource_id: {db_datasource.id} - True")
                    else:
                        print(f"datasource_id: {db_datasource.id} - False")
            except KeyError:
                print(f"Datasourceid: {db_datasource.id} not have pip - False")

        else:
            print(f"formatid: {db_datasource.format_id} not required pip - True")









def test_jay_lost_background_from_S3():
    with open('/Users/phamhanh/Desktop/bg_datasource_ids.json') as json_file:
        data = json.load(json_file)

    with open('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt', "w") as f:
        datasource_ids = get_all_datasource_valid(thread_session)
        for db_datasource in datasource_ids:
            if 'bg_720_file_name' in db_datasource.ext.keys():
                bg_720_file_name = db_datasource.ext['bg_720_file_name']
                key1 = f"videos/{bg_720_file_name}"
                result1 = existing_on_s3(key1)
                if result1 == 1:
                    joy_check = db_datasource.id in data
                    if joy_check == 1:
                        joy_xinh = joy_xinh + f"Datasource id: [{db_datasource.id}] -['bg_720_file_name'] - {result1}- [{db_datasource.created_at}]- [jay_wrong];\n"

                    else:
                        joy_xinh = f"Datasource id: [{db_datasource.id}] -['bg_720_file_name'] - {result1}- [{db_datasource.created_at}]- [jay_true];\n"

                else:
                    joy_check = db_datasource.id in data
                    if joy_check == 1:
                        joy_xinh = f"Datasource id: [{db_datasource.id}] -['bg_720_file_name'] - {result1}- [{db_datasource.created_at}]- [jay_true];\n"

                    else:
                        joy_xinh = f"Datasource id: [{db_datasource.id}] -['bg_720_file_name'] - {result1}- [{db_datasource.created_at}]- [jay_missing];\n"

            else:
                joy_check = db_datasource.id in data
                if joy_check == 1:
                    joy_xinh = f"{db_datasource.id}- [{db_datasource.created_at}]- not have background- [jay_true];\n"
                else:
                    joy_xinh = f"{db_datasource.id}- [{db_datasource.created_at}]- not have background- [jay_missing];\n"
            k = joy_xinh
            print(k)
            f.write(k + "\n")


if __name__ == "__main__":
    datasource_ids = [
        "7175F299C2164227A25A6FD9BF8C94AD",
        "1580ED2629A143C6B9446D80DB39D224",
        "472C25E944B3453AA9B4E1F83744DCEB"
    ]
    for datasource_id in datasource_ids:
        datasource_id = [datasource_id]
        print("\n ---", datasource_id, "--- \n")

        checking_lost_datasource_filename_from_S3(datasource_id)
        checking_lost_datasource_image_from_S3(datasource_id)
        checking_lost_datasource_background_from_S3(datasource_id)
        checking_lost_pip_from_S3(datasource_id)
