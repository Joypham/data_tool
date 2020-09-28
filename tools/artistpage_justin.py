from google_spreadsheet_api.function import get_df_from_speadsheet, get_list_of_sheet_title,update_value
from google_spreadsheet_api.create_new_sheet_and_update_data_from_df import creat_new_sheet_and_update_data_from_df
from tools import get_uuid4
import pandas as pd
import time


gsheet_id = input(f"\n Input gsheet_id: ").strip()

def check_youtube_url_mp3():
    '''
    TrackID	Memo	URL_to_add	Type	Assignee
                                        no need to check
    not null	added	length = 43	    C/D/Z
    not null	not found	none	none
    :return:
    '''
    sheet_name = 'MP_3'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)

    original_df['len'] = original_df['url_to_add'].apply(lambda x: len(x))
    youtube_url_mp3 = original_df[['track_id', 'Memo', 'url_to_add', 'len', 'Type', 'Assignee']]

    check_youtube_url_mp3 = youtube_url_mp3[~
    ((
             (youtube_url_mp3['track_id'] != '')
             & (youtube_url_mp3['Memo'] == 'added')
             & (youtube_url_mp3['len'] == 43)
             & (youtube_url_mp3['Type'].isin(["c", "d", "z"]))
     ) |
     (
             (youtube_url_mp3['track_id'] != '')
             & (youtube_url_mp3['Memo'] == 'not found')
             & (youtube_url_mp3['url_to_add'] == 'none')
             & (youtube_url_mp3['Type'] == 'none')
     ) |
     (

         (youtube_url_mp3['Assignee'] == 'no need to check')
     ))
    ]

    return check_youtube_url_mp3.track_id.str.upper()


def check_youtube_url_mp4():
    '''
        TrackID	Memo	URL_to_add	Assignee
                                    no need to check
        not null	ok	null
        not null	added	length = 43
        not null	not found	none
        not null	not ok	length = 43
        not null	not ok	none
    :return:
    '''

    sheet_name = 'MP_4'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    original_df['len'] = original_df['url_to_add'].apply(lambda x: len(x))
    youtube_url_mp4 = original_df[['track_id', 'Memo', 'url_to_add', 'len', 'Assignee']]

    check_youtube_url_mp4 = youtube_url_mp4[~
    ((
             (youtube_url_mp4['track_id'] != '')
             & (youtube_url_mp4['Memo'] == 'ok')
             & (youtube_url_mp4['url_to_add'] == '')
     ) |
     (
             (youtube_url_mp4['track_id'] != '')
             & (youtube_url_mp4['Memo'] == 'added')
             & (youtube_url_mp4['len'] == 43)
     ) |
     (
             (youtube_url_mp4['track_id'] != '')
             & (youtube_url_mp4['Memo'] == 'not found')
             & (youtube_url_mp4['url_to_add'] == 'none')
     ) |
     (
             (youtube_url_mp4['track_id'] != '')
             & (youtube_url_mp4['Memo'] == 'not ok')
             & (youtube_url_mp4['len'] == 43)
     ) |
     (
             (youtube_url_mp4['track_id'] != '')
             & (youtube_url_mp4['Memo'] == 'not ok')
             & (youtube_url_mp4['url_to_add'] == 'none')
     ) |
     (youtube_url_mp4['Assignee'] == 'no need to check')
     )
    ]
    return check_youtube_url_mp4.track_id.str.upper()


def check_version():
    '''
    TrackID	URL	Remix_Artist
    not null	length = 43	not null
    not null	null	null

    TrackID	URL2	Venue
    not null	length = 43	not null
    not null	null	null
    '''

    sheet_name = 'Version_done'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)

    original_df['len_remix_url'] = original_df['Remix_url'].apply(lambda x: len(x))
    original_df['len_live_url'] = original_df['Live_url'].apply(lambda x: len(x))
    youtube_url_version = original_df[
        ['track_id', 'Remix_url', 'Remix_artist', 'Live_url', 'Live_venue', 'len_remix_url', 'len_live_url']]

    check_version = youtube_url_version[~
    (((
              (youtube_url_version['track_id'] != '')
              & (youtube_url_version['len_remix_url'] == 43)
              & (youtube_url_version['Remix_artist'] != '')
      ) |
      (
              (youtube_url_version['track_id'] != '')
              & (youtube_url_version['Remix_url'] == '')
              & (youtube_url_version['Remix_artist'] == '')
      )) &
     ((
              (youtube_url_version['track_id'] != '')
              & (youtube_url_version['len_live_url'] == 43)
              & (youtube_url_version['Live_venue'] != '')
      ) |
      (
              (youtube_url_version['track_id'] != '')
              & (youtube_url_version['Live_url'] == '')
              & (youtube_url_version['Live_venue'] == '')
      )))
    ]
    return check_version.track_id.str.upper()


def check_album_image():
    '''
        AlbumUUID	Memo	URL_to_add	Assignee
                                        no need to check
        not null	ok	null
        not null	added	not null
        not null	not found	none
    :return:
    '''
    sheet_name = 'Album_image'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    album_image = original_df[['Album_uuid', 'Memo', 'url_to_add', 'Assignee']]

    check_album_image = album_image[~
    ((
             (album_image['Album_uuid'] != '')
             & (album_image['Memo'] == 'ok')
             & (album_image['url_to_add'] == '')
     ) |
     (
             (album_image['Album_uuid'] != '')
             & (album_image['Memo'] == 'added')
             & (album_image['url_to_add'] != '')
     ) |
     (
             (album_image['Album_uuid'] != '')
             & (album_image['Memo'] == 'not found')
             & (album_image['url_to_add'] == 'none')
     ) |
     (
         (album_image['Assignee'] == 'no need to check')
     ))
    ]

    return check_album_image.Album_uuid.str.upper()


def check_artist_image():
    '''
        ArtistTrackUUID	Memo	URL_to_add	Assignee
                                            no need to check
        not null	ok	null
        not null	added	not null
    :return:
    '''
    sheet_name = 'Artist_image'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    artist_image = original_df[['Artist_uuid', 'Memo', 'url_to_add', 'Assignee']]

    check_artist_image = artist_image[~
    ((
             (artist_image['Artist_uuid'] != '')
             & (artist_image['Memo'] == 'ok')
             & (artist_image['url_to_add'] == '')
     ) |
     (
             (artist_image['Artist_uuid'] != '')
             & (artist_image['Memo'] == 'added')
             & (artist_image['url_to_add'] != '')
     ) |
     (
         (artist_image['Assignee'] == 'no need to check')
     ))
    ]
    return check_artist_image.Artist_uuid.str.upper()


def check_album_wiki():
    '''
        AlbumUUID	Memo	URL_to_add	Content_to_add	Assignee
                                                        no need to check
        not null	ok	null	null
        not null	added	https://en.wikipedia.org/%	not null
        not null	not found	none	none
        not null	not ok	https://en.wikipedia.org/%	not null
        not null	not ok	none	none
    :return:
    '''
    sheet_name = 'Album_wiki'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    album_wiki = original_df[['Album_uuid', 'Memo', 'url_to_add', 'Content_to_add', 'Assignee']]

    check_album_wiki = album_wiki[~
    ((
             (album_wiki['Album_uuid'] != '')
             & (album_wiki['Memo'] == 'ok')
             & (album_wiki['url_to_add'] == '')
             & (album_wiki['Content_to_add'] == '')
     ) |
     (
             (album_wiki['Album_uuid'] != '')
             & (album_wiki['Memo'] == 'added')
             & (album_wiki['url_to_add'].str[:25] == 'https://en.wikipedia.org/')
             & (album_wiki['Content_to_add'] != '')
     ) |
     (
             (album_wiki['Album_uuid'] != '')
             & (album_wiki['Memo'] == 'not found')
             & (album_wiki['url_to_add'] == 'none')
             & (album_wiki['Content_to_add'] == 'none')
     ) |
     (
             (album_wiki['Album_uuid'] != '')
             & (album_wiki['Memo'] == 'not ok')
             & (album_wiki['url_to_add'].str[:25] == 'https://en.wikipedia.org/')
             & (album_wiki['Content_to_add'] != '')
     ) |
     (
             (album_wiki['Album_uuid'] != '')
             & (album_wiki['Memo'] == 'not ok')
             & (album_wiki['url_to_add'] == 'none')
             & (album_wiki['Content_to_add'] == 'none')
     ) |
     (
         (album_wiki['Assignee'] == 'no need to check')
     ))
    ]
    return check_album_wiki.Album_uuid.str.upper()


def check_artist_wiki():
    '''
        Artist_uuid	Memo	URL_to_add	Assignee
                    no need to check
        not null	ok	null
        not null	added	https://en.wikipedia.org/%
        not null	not found	none
        not null	not ok	https://en.wikipedia.org/%
        not null	not ok	none
    :return:
    '''

    sheet_name = 'Artist_wiki'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    artist_wiki = original_df[['Artist_uuid', 'Memo', 'url_to_add', 'Assignee']]

    check_artist_wiki = artist_wiki[~
    ((
             (artist_wiki['Artist_uuid'] != '')
             & (artist_wiki['Memo'] == 'ok')
             & (artist_wiki['url_to_add'] == '')
     ) |
     (
             (artist_wiki['Artist_uuid'] != '')
             & (artist_wiki['Memo'] == 'added')
             & (artist_wiki['url_to_add'].str[:25] == 'https://en.wikipedia.org/')
     ) |
     (
             (artist_wiki['Artist_uuid'] != '')
             & (artist_wiki['Memo'] == 'not found')
             & (artist_wiki['url_to_add'] == 'none')
     ) |
     (
             (artist_wiki['Artist_uuid'] != '')
             & (artist_wiki['Memo'] == 'not ok')
             & (artist_wiki['url_to_add'].str[:25] == 'https://en.wikipedia.org/')
     ) |
     (
             (artist_wiki['Artist_uuid'] != '')
             & (artist_wiki['Memo'] == 'not ok')
             & (artist_wiki['url_to_add'] == 'none')
     ) |
     (
         (artist_wiki['Assignee'] == 'no need to check')
     ))
    ]
    return check_artist_wiki.Artist_uuid.str.upper()


def check_box():
    # Check all element:
    list_of_sheet_title = get_list_of_sheet_title(gsheet_id)

    if 'MP_3' in list_of_sheet_title:
        youtube_url_mp3 = check_youtube_url_mp3().to_numpy().tolist()
    else:
        youtube_url_mp3 = ["MP_3 not found"]

    if 'MP_4' in list_of_sheet_title:
        youtube_url_mp4 = check_youtube_url_mp4().to_numpy().tolist()
    else:
        youtube_url_mp4 = ["MP_4 not found"]

    if 'Version_done' in list_of_sheet_title:
        version = check_version().to_numpy().tolist()
    else:
        version = ["Version_done not found"]

    if 'Album_image' in list_of_sheet_title:
        album_image = check_album_image().to_numpy().tolist()
    else:
        album_image = ["Album_image not found"]

    if 'Artist_image' in list_of_sheet_title:
        artist_image = check_artist_image().to_numpy().tolist()
    else:
        artist_image = ["Artist_image not found"]

    if 'Album_wiki' in list_of_sheet_title:
        album_wiki = check_album_wiki().to_numpy().tolist()
    else:
        album_wiki = ["Album_wiki not found"]

    if 'Artist_wiki' in list_of_sheet_title:
        artist_wiki = check_artist_wiki().to_numpy().tolist()
    else:
        artist_wiki = ["Artist_wiki not found"]

    # Convert checking element result to df:
    items = []
    status = []
    comment = []

    dict_value = [youtube_url_mp3, youtube_url_mp4, version, album_image, artist_image, album_wiki, artist_wiki]
    dict_key = ['youtube_url_mp3', 'youtube_url_mp4', 'version', 'album_image', 'artist_image', 'album_wiki',
                'artist_wiki']
    dict_result = dict(zip(dict_key, dict_value))
    for i, j in dict_result.items():
        if not j:
            status.append('ok')
            comment.append(None)
            items.append(i)
        else:
            status.append('not ok')
            comment.append(j)
            items.append(i)
    print(comment)

    d = {'items': items, 'status': status, 'comment': comment}
    df = pd.DataFrame(data=d).astype(str)
    print(df)

    if 'jane_to_check_result' in list_of_sheet_title:
        update_value(df.values.tolist(),'jane_to_check_result!A2',gsheet_id)
    else:
        creat_new_sheet_and_update_data_from_df(df,gsheet_id,'jane_to_check_result')

    return df


def process_MP_4():
    '''
    Memo = not ok and url_to_add = 'none' => set_datasource_valid = -1202
    Memo = not ok and url_to_add not null => crawl mode replace
    '''
    # checking = 'not ok' in check_box().status.drop_duplicates().tolist()
    # if checking == 1:
    #     return print("Please recheck check_box is not ok")
    # else:
    sheet_name = 'MP_4'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name)
    youtube_url_mp4 = original_df[['track_id', 'Memo', 'url_to_add', 'MP4_link']]
    mp4_file_to_process = youtube_url_mp4[(youtube_url_mp4['Memo'] == 'not ok') | (youtube_url_mp4['Memo'] == 'added')].reset_index().drop_duplicates(subset=['track_id'],keep='first')  # remove duplicate df by column (reset_index before drop_duplicate: because of drop_duplicate default reset index)
    # print(mp4_file_to_process)
    row_index = mp4_file_to_process.index
    with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
        for i in row_index:
            memo = mp4_file_to_process.Memo.loc[i]
            # id = get_uuid4()
            new_youtube_url = mp4_file_to_process.url_to_add.loc[i]
            trackid = mp4_file_to_process.track_id.loc[i]
            old_youtube_url = mp4_file_to_process.MP4_link.loc[i]

            if memo == "not ok" and new_youtube_url == "none":
                print(trackid, '---', new_youtube_url, '---', old_youtube_url)
            else:
                continue

            #     query = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values ('{id}','{trackid}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','keep both' ,'$.youtube_url','{youtube_url}','$.data_source_format_id','7F8B6CD82F28437888BD029EFDA1E57F','$.concert_live_name','{place}','$.year','{year}','$.PIC', \"Joy_xinh\"),999);\n"
            # elif action_type == "COVER_VIDEO":
            #     query = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values ('{id}','{trackid}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','keep both' ,'$.youtube_url','{youtube_url}','$.data_source_format_id','F5D2FE4A15FB405E988A7309FD3F9920','$.covered_artist_name','{artist_cover}','$.year','{year}','$.PIC', \"Joy_xinh\"),999);\n"
            # elif action_type == "FANCAM_VIDEO":
            #     query = f"insert into crawlingtasks(Id,ObjectID ,ActionId, TaskDetail, Priority) values ('{id}','{trackid}' ,'F91244676ACD47BD9A9048CF2BA3FFC1',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()),'$.when_exists','keep both' ,'$.youtube_url','{youtube_url}','$.data_source_format_id','DDC08421CAEB4E918F3FE373209020F9','$.concert_live_name','{place}','$.year','{year}','$.PIC', \"Joy_xinh\"),999);\n"
            # else:
            #     continue
            # f.write(query)

            # print(trackid)


if __name__ == "__main__":
    start_time = time.time()
    pd.set_option("display.max_rows", None, "display.max_columns", 30, 'display.width', 500)
    # INPUT HERE
    # Justin requirement: https://docs.google.com/spreadsheets/d/1LClklcO0OEMmQ1iaCZ34n1hhjlP1lIBj7JMjm2qrYVw/edit#gid=0
    # Jane requirement: https://docs.google.com/spreadsheets/d/1nm7DRUX0v1zODohS6J5LTDHP2Rew-OxSw8qN5FiplVk/edit#gid=653576103
    # 'https://docs.google.com/spreadsheets/d/17J5nC9HnX53U5htuxZVAsKFPh3SCaZaZ7iMKXtE44D8'
    # gsheet_id = '1k1-qrQxZV00ImOsdUv7nsONQBTc_5_45-T580AfTkEc'

    # Start tools:
    check_box()
    # process_MP_4()

    print("--- %s seconds ---" % (time.time() - start_time))