import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    ADMINS = ["bulatsharipov240@gmail.com"]

    TASKS_PER_PAGE = 3
    LANGUAGES = ["en", "ru"]
