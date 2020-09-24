from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/token.pickle'):
        with open('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


def gspread_values(gsheet_id, sheet_name):
    # Call the Sheets API
    sheet = service().spreadsheets()
    result = sheet.values().get(spreadsheetId=gsheet_id,
                                range=sheet_name).execute()
    values = result.get('values', [])
    return values


def add_sheet(gsheet_id, sheet_name):
    try:
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                        'tabColor': {
                            'red': 0.44,
                            'green': 0.99,
                            'blue': 0.50
                        }
                    }
                }
            }]
        }

        response = service().spreadsheets().batchUpdate(
            spreadsheetId=gsheet_id,
            body=request_body
        ).execute()

        return response
    except Exception as e:
        print(e)


def update_value(list_result: list, range_to_update: str, gsheet_id: str):
    body = {
        'values': list_result  # list_result is array 2 dimensional (2D)
    }
    result = service().spreadsheets().values().update(
        spreadsheetId=gsheet_id, range=range_to_update,
        valueInputOption='RAW', body=body).execute()


def get_df_from_speadsheet(gsheet_id: str, sheet_name: str):
    # need to optimize to read df from column_index: int = 0 (default = 0)
    data = gspread_values(gsheet_id, sheet_name)
    column = data[0]
    check_fistrow = data[1]
    x = len(column) - len(check_fistrow)
    k = [None] * x
    check_fistrow.extend(k)  # if only have column name but all data of column null =>> error
    row = data[2:]
    row.insert(0, check_fistrow)
    df = pd.DataFrame(row, columns=column).apply(lambda x: x.str.strip()).fillna(value='').astype(str)
    # df.apply(lambda x: x.str.strip()).fillna(value='').astype(str)
    return df


def get_list_of_sheet_title(gsheet_id: str):
    sheet_metadata = service().spreadsheets().get(spreadsheetId=gsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    list_of_sheet_title = []
    for i in sheets:
        list_of_sheet_title.append(i['properties']['title'])
    return list_of_sheet_title


def get_test(gsheet_id: str):
    sheet_metadata = service().spreadsheets().get(spreadsheetId=gsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    result = sheets.values()
    print(result)

    # values = result.get('values', [])
    return result

    # sheet = service().spreadsheets()
    # result = sheet.values().get(spreadsheetId=gsheet_id,
    #                             range=sheet_name).execute()
    # values = result.get('values', [])

# if __name__ == "__main__":
#     pd.set_option("display.max_rows", 100, "display.max_columns", 15, 'display.width', 1000)
#
#     # INPUT HERE:
#     # Input_url 'https://docs.google.com/spreadsheets/d/1Hf8F6o-UMZZix22U-PUqMF31zOLKEM7L5sD7Xuwbpm8/edit#gid=1133448069'
#
#     gsheet_id = '1s7kNSz_dF_k7dVxMpSezKdENCbnYpf5mgSiDpiOs0Mw'  # AT page
#     sheet_name = 'MP3X'
#
#
#     # start tool:
#     # get_list_of_sheet_title(gsheet_id)
#
#
#     gspread_values(gsheet_id, 'MP3X')
