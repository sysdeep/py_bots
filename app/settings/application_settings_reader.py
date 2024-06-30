import os

from app.settings.application_settings import ApplicationSettings


class ApplicationSettingsReader:

    @classmethod
    def read_from_env(cls) -> ApplicationSettings:

        token = os.environ.get("TOKEN")
        if not token:
            raise Exception("TOKEN env is not found")

        return ApplicationSettings(token=token)
