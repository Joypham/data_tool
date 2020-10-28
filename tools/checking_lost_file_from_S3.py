
from core.aws.aws_config import AWSConfig
from core.aws.s3.aws_s3 import existing_on_s3
from core.crud.sql.datasource import get_all_by_ids


def checking_lost_datasource_from_S3(datasource_ids: list):
    print("start")
    db_datasources = get_all_by_ids(datasource_ids)

    for db_datasource in db_datasources:
        if db_datasource.is_video == 1:
            key = f"videos/{db_datasource.file_name}"

        else:
            key = f"audio/{db_datasource.file_name}"
        result = existing_on_s3(key)
        print(f"Datasource id: [{db_datasource.id}] - {result}")
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




if __name__ == "__main__":
    datasource_ids = [
        "049429A3FCA64BAAB171385879BF9EE1",
        "1114915809844945829C20CC8AA63419",
        "47E552801EE44B528D58C0B37C63A37D",
        "69BF366D2BF34744B7C1587CBE091F7B",
        "8400B16D30744B07B12E1E28F3F97750",
        "A72500FB63C449358EF2F82268DF4478",
        "CD357170D33A43E8B72DD34F25DCC9B2",
        "D85E5D68879E49BAA29FE58F0575F997",
        "000066A084BC4312AAC68A42B49DC1A5",
        "0000792E4E7E4363873058939B666584"
    ]
    checking_lost_datasource_image_from_S3(datasource_ids)
