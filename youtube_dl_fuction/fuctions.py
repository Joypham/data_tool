import youtube_dl
import time
import traceback

def get_title_uploader_from_youtube_url(youtube_url: str):
    print(youtube_url)

    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    result = ydl.extract_info(
        youtube_url,
        download=False  # We just want to extract the info
    )
    joy = {"youtube_url": youtube_url, "uploader": result.get('uploader'), "youtube_title": result.get('title')}
    return joy


if __name__ == "__main__":
    start_time = time.time()

    youtube_url = "https://www.youtube.com/watch?v=x_XlqZk1jW0"

    get_title_uploader_from_youtube_url(youtube_url)

    print("--- %s seconds ---" % (time.time() - start_time))
