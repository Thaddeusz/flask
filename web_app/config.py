import os

class config:
    SECRET_KEY = '3badce9f82d5d3567d83e489552ad555'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIl_USERNAME = os.environ.get("EMAIL_USER")
    MAIl_PASSWORD = os.environ.get("EMAIL_PASS") 