import youtube_dl
import time
from youtube_dl.utils import DownloadError
from core import youtube_com_cookies_path
import json
import traceback

def get_title_uploader_from_youtube_url(youtube_url: str):
    print(youtube_url)
    ytdl_options = {
        "cachedir": False,
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
        youtube_info_result = {"youtube_url": youtube_url, "uploader": result.get('uploader'), "youtube_title": result.get('title')}
    except DownloadError as ex:
        youtube_info_result = {"youtube_url": youtube_url, "uploader": f"{ex}", "youtube_title": f"{ex}"}
    except:  # noqa
        youtube_info_result = {"youtube_url": youtube_url, "uploader": "Error: Unknown error", "youtube_title": "Error: Unknown error"}
    return youtube_info_result


if __name__ == "__main__":
    start_time = time.time()

    youtube_url = "https://www.youtube.com/watch?v=x_XlqZk1jW0"

    get_title_uploader_from_youtube_url(youtube_url)

    print("--- %s seconds ---" % (time.time() - start_time))
