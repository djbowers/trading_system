import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    PRICE_DIR = os.path.join(DATA_DIR, 'price')


class TestingConfig(Config):
    TESTING = True
    TEST_DIR = os.path.join(BASE_DIR, 'test')
    DATA_DIR = os.path.join(TEST_DIR, 'data')
    PRICE_DIR = os.path.join(DATA_DIR, 'price')
    SYMBOLS = ['BTC', 'ETH', 'LTC']


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
