# https://developers.google.com/sheets/api/quickstart/python

from google_spreadsheet_api.function import update_value
from core.crud.get_df_from_query import get_df_from_query
from core.crud.sql.external_identity import get_artists_from_album_ituneid
from google_spreadsheet_api.function import get_df_from_speadsheet
import pandas as pd
import time


def export_artist_contribution(gsheet_id: str, sheet_name: str):
    pd.set_option("display.max_rows", None, "display.max_columns", 60, 'display.width', 1000)
    df = get_df_from_speadsheet('1wMLmbaY3ZJiPDU2uekzfVVLjwHOzGJ2TpYFNCWTNqAE', 'Youtube collect_experiment')
    album_ituneid = df[(df.Itunes_ID != '')
                       & (df.Itunes_ID != 'Itunes_ID')
                       & (df.Itunes_ID.notnull())
                       ]['Itunes_ID'].drop_duplicates(keep='first').tolist()

    # Update data to gsheet_id
    column_name = get_df_from_query(get_artists_from_album_ituneid(album_ituneid)).columns.values.tolist()
    list_result = get_df_from_query(get_artists_from_album_ituneid(album_ituneid)).astype(
        str).values.tolist()  # transfer data_frame to 2D list
    list_result.insert(0, column_name)

    range_to_update = f"{sheet_name}!A1"
    update_value(list_result, range_to_update, gsheet_id)


if __name__ == "__main__":
    start_time = time.time()
    # INPUT HERE
    # 'https://docs.google.com/spreadsheets/d/1Ck9O771xM7VArdaYxbHTVtp4kRtHzPn57EDDId0cHJc/edit#gid=0'
    gsheet_id = '1YlHaVJrLUZumeuhfX21e1cmbtXmEtKNpRUIuONJoxd0'
    sheet_name = 'Artist List'
    export_artist_contribution(gsheet_id, sheet_name)
    print("--- %s seconds ---" % (time.time() - start_time))
