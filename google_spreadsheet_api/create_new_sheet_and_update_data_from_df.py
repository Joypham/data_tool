# https://developers.google.com/sheets/api/quickstart/python

from google_spreadsheet_api.function import add_sheet
from google_spreadsheet_api.function import update_value


def creat_new_sheet_and_update_data_from_df(df: object, gsheet_id: str, new_sheet_name: str):

    '''

    :param df: dataframe column_type: not date_time and fillna before update value to gsheet, Eg: df.fillna(value='None').astype({"created_at": 'str'})
    :param gsheet_id:
    :param new_sheet_name:
    :return:
    '''
    column_name = df.columns.values.tolist()
    list_result = df.values.tolist()  # transfer data_frame to 2D list
    list_result.insert(0, column_name)

    add_sheet(gsheet_id, new_sheet_name)
    range_to_update = f"{new_sheet_name}!A1"
    update_value(list_result, range_to_update, gsheet_id)   # validate_value type: object, int, category... NOT DATETIME
    return print("\n complete create new sheet and update data")
