from core.crud.sql.album import get_album_wiki
from core.crud.sql.track import get_track_wiki, get_track_lyric
from core.crud.sql.crawlingtask import get_crawl_artist_image_status, get_artist_image_cant_crawl
from core.crud.get_df_from_query import get_df_from_query

from google_spreadsheet_api.function import add_sheet
from google_spreadsheet_api.function import update_value
from google_spreadsheet_api.function import get_df_from_speadsheet
from google_spreadsheet_api.create_new_sheet_and_update_data_from_df import creat_new_sheet_and_update_data_from_df

import time
import pandas as pd
import numpy as np


def upload_album_wiki():
    df = get_df_from_speadsheet(gsheet_id, sheet_name)
    album_uuid = df[(df.albumuuid != '') & (df.albumuuid != 'Album_UUID') & (df.albumuuid.notnull())][
        'albumuuid'].tolist()
    df_album_wiki = get_df_from_query(get_album_wiki(album_uuid))
    print("file to upload \n", df_album_wiki)

    time.sleep(3)
    print("\n Updating data")
    creat_new_sheet_and_update_data_from_df(df_album_wiki, gsheet_id, 'wiki')


def upload_track_wiki():
    # Step 1: get data
    df = get_df_from_speadsheet(gsheet_id, sheet_name)
    track_id = tuple(df[(df.TrackId != '') & (df.TrackId != 'TrackId') & (df.TrackId.notnull())]['TrackId'].tolist())
    df_track_wiki = get_df_from_query(get_track_wiki(track_id))
    print("file to upload \n", df_track_wiki)

    time.sleep(3)
    print("\n Updating data")
    creat_new_sheet_and_update_data_from_df(df_track_wiki, gsheet_id, 'wiki')


def upload_track_lyrics():
    # Step 1: get data
    df = get_df_from_speadsheet(gsheet_id, sheet_name)
    trackid = tuple(df[(df.TrackId != '') & (df.TrackId != 'TrackId') & (df.TrackId.notnull())]['TrackId'].tolist())
    df_track_lyric = get_df_from_query(get_track_lyric(trackid))

    print("file to upload \n", df_track_lyric)

    time.sleep(3)
    print("\n Updating data")
    creat_new_sheet_and_update_data_from_df(df_track_lyric, gsheet_id, 'lyrics')


def automate_check_crawl_artist_image_status():  # need to optimize
    commit_message = input(f"\n Do you complete crawling_tasks insertion ?: True or False:")

    if commit_message == '1':
        count = 0
        while True and count < 300:
            df1 = get_df_from_query(get_crawl_artist_image_status())
            result = df1[
                         (df1.status != 'complete')
                         & (df1.status != 'incomplete')
                         ].status.tolist() == []
            if result == 1:
                print(df1)
                break
            else:
                count += 1
                time.sleep(5)
                print(count, "-----", result)

    else:
        print("Please insert crawling_tasks")


def crawl_artist_image_singlepage():
    # STEP 1: Get_query_to_crawl
    df = get_df_from_speadsheet(gsheet_id, sheet_name)
    filter_df = df[(df.Artist_UUID != 'ArtistName')  # filter df by conditions
                   & (df.Artist_UUID != 'Artist_UUID')
                   & (df.image_url.notnull())
                   & (df.s12 == 'missing')
                   & (df.image_url != '')].reset_index().drop_duplicates(subset=['Artist_UUID'],
                                                                         keep='first')  # remove duplicate df by column (reset_index before drop_duplicate: because of drop_duplicate default reset index)
    print("List artist to crawl image \n ", filter_df[['ArtistName', 'Artist_UUID', 's12', 'image_url']], "\n")

    row_index = filter_df.index
    with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
        for i in row_index:
            x = filter_df['Artist_UUID'].loc[i]
            y = filter_df['image_url'].loc[i]
            query = f"insert into crawlingtasks(Id, ActionId,objectid ,TaskDetail, Priority) values (uuid4(), 'OA9CPKSUT6PBGI1ZHPLQUPQCGVYQ71S9','{x}',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.url','{y}','$.object_type',\"artist\",'$.when_exists',\"replace\",'$.PIC',\"Joy_xinh\"),99);"
            print(query)
            f.write(query + "\n")

    # STEP 2: automation check crawl_artist_image_status then export result:
    automate_check_crawl_artist_image_status()
    # STEP 3: upload artist image cant upload
    artist_uuid = filter_df['Artist_UUID'].tolist()
    df_artist_image_cant_upload = get_df_from_query(get_artist_image_cant_crawl(artist_uuid))
    joy = df_artist_image_cant_upload['name'].tolist() == []
    new_sheet_name = 'artist image cant upload joy test'
    if joy == 1:
        list_result = [['Upload thành công 100% nhé các em ^ - ^']]
        add_sheet(gsheet_id, new_sheet_name)
        update_value(list_result, f"{new_sheet_name}!A1", gsheet_id)
    else:
        creat_new_sheet_and_update_data_from_df(df_artist_image_cant_upload, gsheet_id, new_sheet_name)


def crawl_artist_image_albumpage():
    # STEP 1: Get_query_to_crawl
    df = get_df_from_speadsheet(gsheet_id, sheet_name)
    filter_df = df[(df.A12 == 'missing')  # filter df by conditions
                   & (df.image_url.notnull())
                   & (df.image_url != '')
                   ].reset_index().drop_duplicates(subset=['Artist_UUID'],
                                                   keep='first')  # remove duplicate df by column (reset_index before drop_duplicate: because of drop_duplicate default reset index)
    print("List artist to crawl image \n ", filter_df[['ArtistName', 'Artist_UUID', 'A12', 'image_url']], "\n")

    row_index = filter_df.index
    with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
        for i in row_index:
            x = filter_df['Artist_UUID'].loc[i]
            y = filter_df['image_url'].loc[i]
            query = f"insert into crawlingtasks(Id, ActionId,objectid ,TaskDetail, Priority) values (uuid4(), 'OA9CPKSUT6PBGI1ZHPLQUPQCGVYQ71S9','{x}',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.url','{y}','$.object_type',\"artist\",'$.when_exists',\"replace\",'$.PIC',\"Joy_xinh\"),99);"
            print(query)
            f.write(query + "\n")

    # STEP 2: automation check crawl_artist_image_status then export result:
    automate_check_crawl_artist_image_status()

    # STEP 3: upload artist image cant upload
    artist_uuid = filter_df['Artist_UUID'].tolist()
    df_artist_image_cant_upload = get_df_from_query(get_artist_image_cant_crawl(artist_uuid))
    joy = df_artist_image_cant_upload['name'].tolist() == []
    new_sheet_name = 'artist image cant upload joy test'
    if joy == 1:
        list_result = [['Upload thành công 100% nhé các em ^ - ^']]
        add_sheet(gsheet_id, new_sheet_name)
        update_value(list_result, f"{new_sheet_name}!A1", gsheet_id)
    else:
        creat_new_sheet_and_update_data_from_df(df_artist_image_cant_upload, gsheet_id, new_sheet_name)


def check_wiki_before_update_data():  # both single page and album page
    df_wiki = get_df_from_speadsheet(gsheet_id, 'wiki')
    df_wiki_filter = df_wiki[(df_wiki.memo == 'added')]
    df_wiki_checking = df_wiki_filter[(df_wiki_filter.url_to_add == '')
                                      | (df_wiki_filter.content_to_add == '')
                                      | (df_wiki_filter.url_to_add.isnull())
                                      | (df_wiki_filter.content_to_add.isnull())].values.tolist()
    result = df_wiki_checking == []
    return result


def update_wiki_result_to_gsheet():  # both single page and album page
    sheet_name = 'wiki'
    df_wiki = get_df_from_speadsheet(gsheet_id, sheet_name)

    conditions = [  # create a list of condition => if true =>> update value tương ứng
        (df_wiki['memo'] == 'not ok'),
        (df_wiki['memo'] == 'added') & (df_wiki.content_to_add.notnull()) & (df_wiki.url_to_add.notnull()),
        True]
    values = ['remove wiki', 'wiki added', None]  # create a list of the values tương ứng với conditions ơ trên
    df_wiki['joy xinh'] = np.select(conditions,
                                    values)  # create a new column and use np.select to assign values to it using our lists as arguments
    column_title = ['Joy note']
    list_result = np.array(df_wiki['joy xinh']).reshape(-1,
                                                        1).tolist()  # Chuyển về list từ 1 chiều về 2 chiều sử dung Numpy
    list_result.insert(0, column_title)
    range_to_update = f"{sheet_name}!K1"

    update_value(list_result, range_to_update, gsheet_id)
    print("update data in gsheet completed")


def update_wiki_singlepage():
    sheet_name = 'wiki'
    # Step 1: checking data
    if check_wiki_before_update_data() == 0:
        print("missing wiki_url or wiki_content")

    # Step 2: Update data in database
    else:
        df_wiki = get_df_from_speadsheet(gsheet_id, sheet_name)
        df_wiki_filter = df_wiki[(df_wiki.memo == 'added') | (df_wiki.memo == 'not ok')]
        row_index = df_wiki_filter.index
        print(row_index)
        with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
            for i in row_index:
                id = df_wiki_filter.id.loc[i]
                memo = df_wiki_filter.memo.loc[i]
                url = df_wiki_filter.url_to_add.loc[i]
                content = df_wiki_filter.content_to_add.loc[i].replace('\'', '\\\'').replace("\"", "\\\"")

                joy_xinh = f"Update tracks set info =  Json_replace(Json_remove(info,'$.wiki'),'$.wiki_url','not ok') where id = '{id}';"
                query = ""
                if memo == "added" and url != "" and content != "":
                    query = f"UPDATE tracks SET info = Json_set(if(info is null,JSON_OBJECT(),info), '$.wiki', JSON_OBJECT('brief', '{content}'), '$.wiki_url','{url}') WHERE id = '{id}';"
                else:
                    query = query
                f.write(joy_xinh + "\n" + query + "\n")
                print(query)

        # Step 3: update gsheet
        update_wiki_result_to_gsheet()


def update_wiki_albumpage():
    sheet_name = 'wiki'
    # Step 1: checking data
    if check_wiki_before_update_data() == 0:
        print("missing wiki_url or wiki_content")

    # Step 2: Update data in database
    else:
        df_wiki = get_df_from_speadsheet(gsheet_id, sheet_name)
        df_wiki_filter = df_wiki[(df_wiki.memo == 'added') | (df_wiki.memo == 'not ok')]
        row_index = df_wiki_filter.index
        print(row_index)
        with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
            for i in row_index:
                uuid = df_wiki_filter.uuid.loc[i]
                memo = df_wiki_filter.memo.loc[i]
                url = df_wiki_filter.url_to_add.loc[i]
                content = df_wiki_filter.content_to_add.loc[i].replace('\'', '\\\'').replace("\"", "\\\"")

                joy_xinh = f"Update albums set info =  Json_replace(Json_remove(info,'$.wiki'),'$.wiki_url','not ok') where uuid = '{uuid}';"
                query = ""
                if memo == "added" and url != "" and content != "":
                    query = f"UPDATE albums SET info = Json_set(if(info is null,JSON_OBJECT(),info), '$.wiki', JSON_OBJECT('brief', '{content}'), '$.wiki_url','{url}') WHERE uuid = '{uuid}';"
                else:
                    query = query
                f.write(joy_xinh + "\n" + query + "\n")
                print(query)

        # Step 3: update gsheet
        update_wiki_result_to_gsheet()


if __name__ == "__main__":
    start_time = time.time()
    pd.set_option("display.max_rows", None, "display.max_columns", 30, 'display.width', 500)
    # INPUT HERE:
    # Input_url 'https://docs.google.com/spreadsheets/d/1vimk9rzzCqx0ySs5NjiT3mipdLGec8-uGdIvOKmpm5w/edit#gid=1785798566'
    gsheet_id = '1vimk9rzzCqx0ySs5NjiT3mipdLGec8-uGdIvOKmpm5w'  # Album page
    sheet_name = '21.09.2020'

    # Input_url 'https://docs.google.com/spreadsheets/d/1t5xEB4Rl1--CVp6CiZzZF-J9FiYAiFizvACUVEPpauk/edit#gid=0'
    # gsheet_id = '1t5xEB4Rl1--CVp6CiZzZF-J9FiYAiFizvACUVEPpauk'  # Single page
    # sheet_name = '21.09.2020'
    # print(joy)

    # Start tool:
    # upload_album_wiki()
    # upload_track_wiki()
    # upload_track_lyrics()

    # crawl_artist_image_singlepage()
    # crawl_artist_image_albumpage()
    # update_wiki_singlepage()
    # update_wiki_albumpage()

    print("\n --- total time to process %s seconds ---" % (time.time() - start_time))
