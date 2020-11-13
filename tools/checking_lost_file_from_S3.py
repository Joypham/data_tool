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
        "0340654DF0C24DFFAD5783E5C1333A53",
        "13E23CE7F4DC467EA716119C79742A75",
        "9CC6E2E0981045EA80E94FB1C646F04D",
        "19C495499D264DFABC7E51E4C200D455",
        "8CC04C7DD82F43D9AB31537918CE8199",
        "8E12668D568B41A5918E7D136DC0AD84",
        "90D4B35BCE4E4EE3AB3DED74385E517A",
        "AA1DCCAD010E4D1A8AFA9F3B19039F59",
        "AB5E431F4D7F417182BEBA1FBA22744D",
        "B0C8073511B043C889C742D21909B4B9",
        "D0DCC99A7D704F6E89FF1660F79292BB",
        "D9CC74D9BADB4723A94347BC361A3751",
        "92DBBD15F8DC416EAEF6A50C4EAA9A2E",
        "7306C4FB7FD74F37B12A304371CBA82D",
        "DBBE70E1A12A4D27B7F0D3313C79B4C7"
    ]
    checking_lost_datasource_from_S3(datasource_ids)
