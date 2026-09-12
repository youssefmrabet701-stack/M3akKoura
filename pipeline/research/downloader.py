import yt_dlp
import sys


def download_video(video_id):
    test=False
    for i in range(3):
        try: 
            #something + id
            url = "https://www.youtube.com/watch?v="+video_id
            #options : format , maybe quality ...
            options = {
                "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "outtmpl": "media/%(id)s.%(ext)s"
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
            test=True
            break
        except Exception:
            print("attempt failed, retrying...")
    if not test:
        print("i give up downloading")
        return 
    else:
        print("done downloading")
        return info["_filename"]
    
if __name__ == "__main__":
    video_id = sys.argv[1]
    download_video(video_id)