import youtube_dl
import time
from youtube_dl.utils import DownloadError
from core.crud.sql.datasource import get_one_youtube_url_and_youtube_uploader_by_youtube_url
from core import youtube_com_cookies_path
import json
from numpy import random
import traceback


def get_raw_title_uploader_from_youtube_url(youtube_url: str):
    ytdl_options = {
        # "cachedir": False,
        "quiet": True,
        "nocheckcertificate": True,
        "restrictfilenames": True,
        "cookiefile": youtube_com_cookies_path,
    }

    try:
        ydl = youtube_dl.YoutubeDL(ytdl_options)

        result = ydl.extract_info(
            youtube_url,
            download=False  # We just want to extract the info
        )
        youtube_info_result = {"youtube_url": youtube_url, "uploader": result.get('uploader'),
                               "youtube_title": result.get('title')}
    except DownloadError as ex:
        youtube_info_result = {"youtube_url": youtube_url, "uploader": f"{ex}", "youtube_title": f"{ex}"}
    except:  # noqa
        youtube_info_result = {"youtube_url": youtube_url, "uploader": "Error: Unknown error",
                               "youtube_title": "Error: Unknown error"}
    x = random.uniform(0.5, 3)
    time.sleep(x)
    return youtube_info_result


def get_raw_title_uploader_from_youtube_url_fixed(youtube_url: str):
    db_datasources = get_one_youtube_url_and_youtube_uploader_by_youtube_url(youtube_url)
    if not db_datasources:
        result = get_raw_title_uploader_from_youtube_url(youtube_url)
        print(result)
    else:
        for db_datasource in db_datasources:
            info = db_datasource.info.get('source', None)
            print(info)




                # youtube_title = info.get('title', None)

        # if db_datasource.id == None:
        #     print("joy xinh")
        # print(db_datasource.id)
        # joy = db_datasource.info.get('source', None)


            # print(f"{db_datasource.id}---{joy}")




        # ydl = youtube_dl.YoutubeDL(ytdl_options)
        #
        # result = ydl.extract_info(
        #     youtube_url,
        #     download=False  # We just want to extract the info
        # )
        # print(json.dumps(result)
        #       )
        # youtube_info_result = {"youtube_url": youtube_url, "uploader": result.get('uploader'),
        #                        "youtube_title": result.get('title')}
    # except DownloadError as ex:
    #     youtube_info_result = {"youtube_url": youtube_url, "uploader": f"{ex}", "youtube_title": f"{ex}"}
    # except:  # noqa
    #     youtube_info_result = {"youtube_url": youtube_url, "uploader": "Error: Unknown error",
    #                            "youtube_title": "Error: Unknown error"}
    # x = random.uniform(0.5, 3)
    # time.sleep(x)
    # return youtube_info_result

if __name__ == "__main__":
    start_time = time.time()
    youtube_urls = [
        "https://www.youtube.com/watch?v=4c1Tii9AT54",
        "https://www.youtube.com/watch?v=8vfM68LVPfE",
        "https://www.youtube.com/watch?v=R5xHTpRThn0",
        "https://www.youtube.com/watch?v=i4ZIo0M5-Gg",
        "https://www.youtube.com/watch?v=6eVuF3PIJCc",
        "https://www.youtube.com/watch?v=ASgldwK5ERI",
        "https://www.youtube.com/watch?v=fPBmJSNSiFY",
        "https://www.youtube.com/watch?v=WdXE8FXbP6k",
        "https://www.youtube.com/watch?v=4UfZQYA_FCk"
    ]
    for youtube_url in youtube_urls:
        print(youtube_url)
        get_raw_title_uploader_from_youtube_url_fixed(youtube_url)
        # get_raw_title_uploader_from_youtube_url(youtube_url)

    t2 = time.time() - start_time
    print(t2)

