import os


class CookiesManager:

    def __init__(self, cookies_file_path=None):
        self.cookies_file_path = cookies_file_path or os.getenv(
            "COOKIES_FILE_PATH", "/app/cookies/cookies.txt"
        )

        if not os.path.exists(self.cookies_file_path):
            raise FileNotFoundError(
                f"No cookies file found at {self.cookies_file_path}. "
                "Export your own YouTube cookies.txt and mount it at this path, "
                "or set COOKIES_FILE_PATH to point at it."
            )

    def get_current_cookie_path(self):
        return self.cookies_file_path
