from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_ID: str
    API_HASH: str
    BOT_NAME: str
    PWD: str
    STATIC_STATUS: str
    STATIC_REG: str
    CONTAINER_TG_NAME: str
    CONTAINER_FAST_NAME: str

    def get_id(self):
        return self.API_ID

    def get_hash(self):
        return self.API_HASH

    def get_bot_name(self):
        return self.BOT_NAME

    def get_pwd(self):
        return self.PWD

    def get_status(self):
        return self.STATIC_STATUS

    def get_reg(self):
        return self.STATIC_REG

    def get_tg_container(self):
        return self.CONTAINER_TG_NAME

    def get_fast_container(self):
        return self.CONTAINER_FAST_NAME

    def get_yt_dlp_options(self):
        return {
            'outtmpl': f'{self.PWD}/media/%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',
            'format': 'bestvideo[height=720][ext=mp4]+bestaudio',
            'merge_output_format': 'mp4',
            'progress_hooks': [],
            'quiet': True,
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "noprogress": True
        }




base_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
