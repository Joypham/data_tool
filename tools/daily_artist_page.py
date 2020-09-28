from google_spreadsheet_api.function import get_df_from_speadsheet
import pandas as pd
import time


def crawl_artist_album_from_artist_ituneid():
    '''
    invert (~) operator: https://stackoverflow.com/questions/17097643/search-for-does-not-contain-on-a-dataframe-in-pandas
    :return:
    '''

    df = get_df_from_speadsheet(gsheet_id, sheet_name).drop_duplicates(subset="external_id",keep= "first")
    row_index = df[
                    (~df.external_id.str.contains(pat='NOT_FOUND', regex=True, na=False))
                    & (df.external_id.notnull())
                    & (df.external_id != '')
                    & (df.external_id != 'None')
                   ].index
    with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
        for i in row_index:
            external_id = df.external_id.loc[i]
            joy_xinh = f"insert into crawlingtasks(Id, ActionId, TaskDetail, Priority) values (uuid4(), '3FFA9CB0E221416288ACFE96B5810BD2',JSON_SET(IFNULL(crawlingtasks.TaskDetail, JSON_OBJECT()), '$.artist_id','{external_id}'),999) ;\n"
            f.write(joy_xinh)


if __name__ == "__main__":
    start_time = time.time()
    pd.set_option("display.max_rows", None, "display.max_columns", 60, 'display.width', 1000)
    # INPUT HERE
    # 'https://docs.google.com/spreadsheets/d/19fCJmPfes3QpsmFwU7W0JOBsJAQNXXkj3huvmFo3zSk/edit#gid=0'
    gsheet_id = '19fCJmPfes3QpsmFwU7W0JOBsJAQNXXkj3huvmFo3zSk'
    sheet_name = 'Artist List'

    crawl_artist_album_from_artist_ituneid()

    print("\n --- total time to process %s seconds ---" % (time.time() - start_time))