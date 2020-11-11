# import cv2
# vidcap = cv2.VideoCapture('https://s3.amazonaws.com/vibbidi-us/videos/video_9857BEF2AD46441A896C49F723DEE157.mp4')
# vidcap.set(cv2.CAP_PROP_POS_MSEC,3000)      # just cue to 20 sec. position
# success,image = vidcap.read()
# if success:
#     cv2.imwrite("frame3sec.jpg", image)     # save frame as JPEG file
#     cv2.imshow('joy',image)
#     cv2.waitKey()

from google_spreadsheet_api.function import get_df_from_speadsheet
import pandas as pd
import time
if __name__ == "__main__":
    start_time = time.time()
    pd.set_option("display.max_rows", None, "display.max_columns", 100, 'display.width', 1000)
    # INPUT HERE
    # Justin requirement: https://docs.google.com/spreadsheets/d/1LClklcO0OEMmQ1iaCZ34n1hhjlP1lIBj7JMjm2qrYVw/edit#gid=0
    # Jane requirement: https://docs.google.com/spreadsheets/d/1nm7DRUX0v1zODohS6J5LTDHP2Rew-OxSw8qN5FiplVk/edit#gid=653576103
    # 'https://docs.google.com/spreadsheets/d/1k1-qrQxZV00ImOsdUv7nsONQBTc_5_45-T580AfTkEc'
    gsheet_id = '1k1-qrQxZV00ImOsdUv7nsONQBTc_5_45-T580AfTkEc'
    sheet_name = 'Version_done'
    original_df = get_df_from_speadsheet(gsheet_id, sheet_name).applymap(str.lower)
    original_df['len_remix_url'] = original_df['Remix_url'].apply(lambda x: len(x))
    original_df['len_live_url'] = original_df['Live_url'].apply(lambda x: len(x))
    original_df['Live_year'] = pd.to_numeric(original_df.Live_year, errors='coerce').astype('Int64').fillna(0)

    original_df = original_df[((1950 <= original_df['Live_year'])& (original_df['Live_year'] <= 2030))]


    print(original_df.head(100))
    # Start tools:
    print("--- %s seconds ---" % (time.time() - start_time))

