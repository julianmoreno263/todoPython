# config.py
POSTGRESQL = "postgresql+psycopg2://postgres:@localhost:5432/blogposts_db"



class Config:
    DEBUG = True
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_PKG_TYPE="full"
    

