from password import password

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{password}@localhost/e_commerce_db'
    CACHE_TYPE = "SimpleCache"
    DEBUG = True