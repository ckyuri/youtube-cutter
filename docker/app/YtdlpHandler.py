import os
import yt_dlp

from Logger import Logger

PID = os.getpid()


class YtdlpHandler:
    destination = None

    def __init__(self, url, cookie_path) -> None:
        self.url = url
        self.yt_id = url.split("watch?v=")[-1]
        self.cookie_path = cookie_path

    def yt_dlp_monitor(self, d):
        if d.get("status") == "finished":
            YtdlpHandler.destination = d.get("filename")

    def yt_dlp_request(self, shouldDownload=False):
        Logger.log(
            f"Attempting to download using cookie {self.cookie_path}",
            PID,
            self.yt_id,
        )

        YtdlpHandler.destination = None

        yt_dlp_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "paths": {
                "home": "/audio/",
            },
            "outtmpl": f"{self.yt_id}.m4a",
            "progress_hooks": [self.yt_dlp_monitor],
            "extractor_args": {
                "youtube": "player_client=web_embedded,android_vr",
            },
            "cookiefile": self.cookie_path,
            "verbose": False,
            "cachedir": "/tmp",
            "nocachedir": True,
            "ignoreerrors": False,
            "js_runtimes": {
                "deno": {
                    "path": "/root/.deno/bin/deno",
                }
            },
        }

        try:
            with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                output = ydl.extract_info(
                    self.url,
                    download=shouldDownload,
                )

            if output is None:
                raise RuntimeError("yt-dlp returned no video information")

            title = output.get("title")
            duration = output.get("duration")

            if shouldDownload and not YtdlpHandler.destination:
                expected_path = f"/audio/{self.yt_id}.m4a"

                if os.path.exists(expected_path):
                    YtdlpHandler.destination = expected_path
                else:
                    raise RuntimeError(
                        f"yt-dlp completed but output file was not found: {expected_path}"
                    )

            if shouldDownload:
                Logger.log(
                    f"yt_dlp_request complete, destination -> {YtdlpHandler.destination}",
                    PID,
                    self.yt_id,
                )

                return {
                    "title": title,
                    "duration": duration,
                    "destfilepath": YtdlpHandler.destination,
                }

        except Exception as e:
            Logger.log(
                f"yt_dlp_request failed: {e}",
                PID,
                self.yt_id,
            )
            raise
