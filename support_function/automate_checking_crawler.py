from core.crud.get_df_from_query import get_df_from_query
from core.crud.sql.crawlingtask import get_crawl_image_status, get_artist_image_cant_crawl
import time


def automate_check_crawl_image_status():  # need to optimize
    commit_message = input(f"\n Do you complete crawling_tasks insertion ?: True or False:")

    if commit_message == '1':
        count = 0
        while True and count < 300:
            df1 = get_df_from_query(get_crawl_image_status())
            result = df1[
                         (df1.status != 'complete')
                         & (df1.status != 'incomplete')
                         ].status.tolist() == []
            if result == 1:
                print('\n', 'Checking crawlingtask status \n', df1, '\n')
                break
            else:
                count += 1
                time.sleep(5)
                print(count, "-----", result)

    else:
        print("Please insert crawling_tasks")