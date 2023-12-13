import yt_dlp as youtube_dl
import threading
import pathlib
import shutil
import time



class Downloader():
    class loggerOutputs:
        def error(msg):
            print("\n[Error]: " + msg)

        def warning(msg):
            print("\n[Warning]: " + msg)

        def debug(msg):
            pass


    def __init__(self, quality=360, folder="", threads=5, zip=False):
        self.quality = quality
        self.folder = folder
        self.threads = threads
        self.zip = zip


    def download(self, link):
        playlist_info = self.get_info(link)
        folder = f"{playlist_info['title']} ({playlist_info['uploader']})"
        self.download_parallel(playlist_info["entries"], folder)

        if self.zip:
            playlistfolder = pathlib.Path(self.folder, folder) if self.folder else folder
            print("\rCreating ZIP File...", end="")
            shutil.make_archive(playlistfolder, "zip", playlistfolder)
            shutil.rmtree(playlistfolder)
            print("\rZIP File Created")


    def get_info(self, link):
        ydl_opts = {
            'extract_flat': "in_playlist",
            'ignoreerrors': True,
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(link)

        return playlist_info


    def download_parallel(self, videos, folder):
        video_threads = []
        thread_values = [0, 0]

        status_thread = threading.Thread(target=self.check_status, args=(video_threads, thread_values))
        for index, video in enumerate(videos):
            video_threads.append(threading.Thread(target=self.download_video, args=(video["url"], folder, index+1, )))
            video_threads[-1].daemon = True
        status_thread.daemon = True
        status_thread.start()

        for thread in video_threads:
            while True:
                if (thread_values[0] - thread_values[1]) < self.threads:
                    thread.start()
                    thread_values[0] += 1
                    break
                time.sleep(1)

        status_thread.join()


    def check_status(self, threads, thread_values):
        start_time = time.time()

        while thread_values[1] < len(threads):
            time.sleep(1)
            finished = 0
            for i in range(thread_values[0]):
                if not threads[i].is_alive():
                    finished += 1
            thread_values[1] = finished
            total_time  = int(time.time() - start_time)
            print(f"\rCompleted: {thread_values[1]} of {len(threads)} in {total_time}s", end="")

        print(f"\rCompleted: {thread_values[1]} of {len(threads)} in {total_time}s")


    def download_video(self, link, folder=None, index=None):
        filename = (f"{index}. " if index else "") + "%(title)s.%(ext)s"
        filefolder = pathlib.Path(self.folder, folder) if folder else None
        filepath = pathlib.Path(filefolder, filename) if filefolder else filename
        filefolder.mkdir(parents=True, exist_ok=True)

        ydl_opts = {
            "format": f"bestvideo[ext=mp4][height<={self.quality}]+bestaudio[ext=m4a]/best[ext=mp4][height<={self.quality}]/best[height<={self.quality}]/best",
            "outtmpl": str(filepath),
            # "writesubtitles": True,
            # "writethumbnail": True,
            "ignoreerrors": True,
            "quiet": True,
            "logger": self.loggerOutputs,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            
d = Downloader()
d.download(input("the play list URL: "))
