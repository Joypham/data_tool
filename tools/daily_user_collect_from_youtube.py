from core.crud.sql.pointlog import collect_from_youtube_query
from core.crud.get_df_from_query import get_df_from_query
from datetime import date
from youtube_dl_fuction.fuctions import get_raw_title_uploader_from_youtube_url
import time
import pandas as pd
from numpy import random

from google_spreadsheet_api.create_new_sheet_and_update_data_from_df import creat_new_sheet_and_update_data_from_df


def daily_user_collect_from_youtube():
    # INPUT HERE:
    # Input_url 'https://docs.google.com/spreadsheets/d/1vlMsEjwBWuuxXecadJsEbBFeuVFAHZSbOz90JhXgioo/edit#gid=1088561556'
    gsheet_id = '1vlMsEjwBWuuxXecadJsEbBFeuVFAHZSbOz90JhXgioo'
    sheet_name = 'Sheet1'
    new_title = f"Daily contribution {date.today()}"
    print(new_title)

    # PROCESS HERE:
    # STEP 1: Get data

    pd.set_option("display.max_rows", None, "display.max_columns", 30, 'display.width', 1000)
    start_time1 = time.time()
    df = get_df_from_query(collect_from_youtube_query())
    df = df.fillna(value='None').astype({"created_at": 'str'})
    df['contribution_url'] = df['contribution_url'].apply(lambda x: x.replace('"', ""))
    # df = df.head(100)


    row_index = df.index
    get_youtube_titles = []
    get_youtube_uploaders = []
    for i in row_index:
        youtube_title = df.youtube_title.loc[i]
        youtube_uploader = df.youtube_uploader.loc[i]
        youtube_url = df.contribution_url.loc[i]
        if youtube_title == 'None':
            get_youtube_info = get_raw_title_uploader_from_youtube_url(youtube_url)

            get_youtube_title = get_youtube_info['youtube_title']
            get_youtube_uploader = get_youtube_info['uploader']

            get_youtube_titles.append(get_youtube_title)
            get_youtube_uploaders.append(get_youtube_uploader)

            x = random.uniform(0.5, 5)
            time.sleep(x)

        else:
            get_youtube_titles.append(youtube_title)
            get_youtube_uploaders.append(youtube_uploader)

    se_youtube_title = pd.Series(get_youtube_titles)
    se_youtube_uploader = pd.Series(get_youtube_uploaders)
    df['get_youtube_title'] = se_youtube_title.values
    df['get_youtube_uploader'] = se_youtube_uploader.values
    print(df)



    # print("\n", "Get data result \n", df)
    # STEP 2: Create sheet and update data to sheet
    creat_new_sheet_and_update_data_from_df(df, gsheet_id, new_title)

    print("\n --- %s seconds ---" % (time.time() - start_time1))


if __name__ == "__main__":
    daily_user_collect_from_youtube()
