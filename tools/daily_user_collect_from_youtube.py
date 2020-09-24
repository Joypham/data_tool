from core.crud.sqlalchemy import collect_from_youtube_query
from core.crud.get_df_from_query import get_df_from_query
from datetime import date
import time
import pandas as pd
from core.crud.sqlalchemy import get_cutoff_date_collect_from_youtube
from google_spreadsheet_api.create_new_sheet_and_update_data_from_df import creat_new_sheet_and_update_data_from_df

if __name__ == "__main__":
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
    print(get_df_from_query(collect_from_youtube_query('2020-09-17')))
    cutoff_date = get_cutoff_date_collect_from_youtube().first().created_at

    joy_xinh = input(f"\n CUT OFF DATE: {cutoff_date} True or False: ")
    if joy_xinh == '1':
        df = get_df_from_query(collect_from_youtube_query(cutoff_date))
        df = df.fillna(value='None').astype({"created_at": 'str'})

    else:
        manual_cutoff_date = input(f"\n MANUAL CUT OFF DATE:")
        df = get_df_from_query(collect_from_youtube_query(manual_cutoff_date))
        df = df.fillna(value='None')

    print(df.dtypes)
    print("\n", "Get data result \n", df)

    # STEP 2: Create sheet and update data to sheet
    creat_new_sheet_and_update_data_from_df(df, gsheet_id, new_title)

    print("\n --- %s seconds ---" % (time.time() - start_time1))
