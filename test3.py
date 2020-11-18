import youtube_dl
import time
from youtube_dl.utils import DownloadError
import traceback


def get_title_uploader_from_youtube_url(youtube_url: str):
    print(youtube_url)
    try:
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        result = ydl.extract_info(
            youtube_url,
            download=False  # We just want to extract the info
        )
        joy = {"youtube_url": youtube_url, "uploader": result.get('uploader'), "youtube_title": result.get('title')}
    except DownloadError as ex:
        joy = {"youtube_url": youtube_url, "uploader": f"{ex}", "youtube_title": f"{ex}"}
    except:  # noqa
        joy = {"youtube_url": youtube_url, "uploader": "Error: Unknown error", "youtube_title": "Error: Unknown error"}
    return joy


if __name__ == "__main__":
    start_time = time.time()

    youtube_url = "https://www.youtube.com/watch?v=9lHxvmkUoho"

    get_youtube_info = get_title_uploader_from_youtube_url(youtube_url)

    get_youtube_title = get_youtube_info['youtube_title']
    get_youtube_uploader = get_youtube_info['uploader']

    print("start")
    print(get_youtube_title)
    print(get_youtube_uploader)

    print("--- %s seconds ---" % (time.time() - start_time))
