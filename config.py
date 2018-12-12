import os


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("GROCMAILK")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # "postgresql+psycopg2://postgres:postgres@localhost/groctest"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ECHO = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("GROCMAILU")
    MAIL_PASSWORD = os.getenv("GROCMAILP")
    MAIL_DEFAULT_SENDER = os.getenv("GROCMAILU")

