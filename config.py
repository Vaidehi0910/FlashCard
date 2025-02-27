import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATION = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir)
    print(SQLITE_DB_DIR)
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True