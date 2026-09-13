import os


class CookiesManager:


    def __init__(self, cookies_file_path=None):
        self.cookies_file_path = cookies_file_path or os.getenv("COOKIES_FILE_PATH")

    def get_current_cookie_path(self):
        if self.cookies_file_path and os.path.exists(self.cookies_file_path):
            return self.cookies_file_path
        return None
