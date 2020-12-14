import youtube_dl
import time
from youtube_dl.utils import DownloadError
from core.crud.sql.datasource import get_one_by_youtube_url
from core import youtube_com_cookies_path
import json
from numpy import random
import traceback


def get_raw_title_uploader_from_youtube_url(youtube_url: str):
    print(youtube_url)
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
        print(json.dumps(result)
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


def test(youtube_url: str):
    print(youtube_url)
    try:
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        result = ydl.extract_info(
            youtube_url,
            download= False  # We just want to extract the info
        )
        joy = {"youtube_url": youtube_url, "uploader": result.get('uploader'), "youtube_title": result.get('title')}
    except DownloadError as ex:
        joy = {"youtube_url": youtube_url, "uploader": f"{ex}", "youtube_title": f"{ex}"}
    except:  # noqa
        joy = {"youtube_url": youtube_url, "uploader": "Error: Unknown error", "youtube_title": "Error: Unknown error"}
    x = random.uniform(0.5, 2)
    time.sleep(x)
    return joy


def get_title_uploader_from_youtube_url(youtube_url: str):
    db_datasource = get_one_by_youtube_url(youtube_url)
    info = db_datasource[0].info
    print(info)


if __name__ == "__main__":
    start_time = time.time()
    youtube_urls = [
        "https://www.youtube.com/watch?v=4c1Tii9AT54",
        # "https://www.youtube.com/watch?v=8vfM68LVPfE",
        # "https://www.youtube.com/watch?v=R5xHTpRThn0",
        # "https://www.youtube.com/watch?v=i4ZIo0M5-Gg",
        # "https://www.youtube.com/watch?v=6eVuF3PIJCc",
        # "https://www.youtube.com/watch?v=ASgldwK5ERI",
        # "https://www.youtube.com/watch?v=fPBmJSNSiFY",
        # "https://www.youtube.com/watch?v=fPBmJSNSiFY",
        # "https://www.youtube.com/watch?v=WdXE8FXbP6k",
        # "https://www.youtube.com/watch?v=4UfZQYA_FCk",
    ]
    for youtube_url in youtube_urls:
        print(get_raw_title_uploader_from_youtube_url(youtube_url))
        # test(youtube_url)
    # t1 = time.time() - start_time
    # start_time = time.time()
    # for youtube_url in youtube_urls:
    #     test(youtube_url)
    # t2 = time.time() - start_time
    # print(t1)
    # print(t2)
