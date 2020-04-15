import os

DATABASE_URI = "{}+mysqlconnector://{}:{}@{}/{}".format(os.getenv('DB_CONNECTION'), os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_DATABASE'))


class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

