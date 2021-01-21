# https://developers.google.com/sheets/api/quickstart/python

from core.crud.get_df_from_query import get_df_from_query
from core.crud.sql.external_identity import get_artists_from_album_ituneid
from google_spreadsheet_api.function import get_df_from_speadsheet, create_new_gsheet, creat_new_sheet_and_update_data_from_df
import pandas as pd
import time

new_gsheet_title = input(f"\n Input new_gsheet_title: ").strip()


def export_artist_contribution():
    pd.set_option("display.max_rows", None, "display.max_columns", 60, 'display.width', 1000)
    df = get_df_from_speadsheet('1wMLmbaY3ZJiPDU2uekzfVVLjwHOzGJ2TpYFNCWTNqAE', 'Youtube collect_experiment')
    album_ituneid = df[(df.Itunes_ID != '')
                       & (df.Itunes_ID != 'Itunes_ID')
                       & (df.Itunes_ID.notnull())
                       ]['Itunes_ID'].drop_duplicates(keep='first').tolist()
    result = get_df_from_query(get_artists_from_album_ituneid(album_ituneid))

    # Update data to gsheet_id
    gsheet_id = create_new_gsheet(new_gsheet_title)
    creat_new_sheet_and_update_data_from_df(result, gsheet_id, 'Artist List')


if __name__ == "__main__":
    start_time = time.time()
    # INPUT HERE
    # 'https://docs.google.com/spreadsheets/d/1Ck9O771xM7VArdaYxbHTVtp4kRtHzPn57EDDId0cHJc/edit#gid=0'
    # 'https://docs.google.com/spreadsheets/d/1wMLmbaY3ZJiPDU2uekzfVVLjwHOzGJ2TpYFNCWTNqAE/edit#gid=0'
    export_artist_contribution()
    print("--- %s seconds ---" % (time.time() - start_time))
