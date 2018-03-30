import utils


class Config:
    """
    Base configuration class. Any configuration parameters that do not change
    between environments should be declared here as global class constants.
    """

    BASE_DIR = utils.BASE_DIR


class DevelopmentConfig(Config):
    """
    This configuration is for development environments. It enables debugging and
    potential future features for developers.
    """

    DATA_DIR = utils.join_paths(Config.BASE_DIR, 'data')
    SYMBOLS = []


class TestingConfig(Config):
    """
    This configuration will be used for testing purposes, including unit tests.
    """

    DATA_DIR = utils.join_paths(Config.BASE_DIR, 'tests/data')
    SYMBOLS = ['BTC', 'ETH', 'LTC']


class ProductionConfig(Config):
    """
    This configuration will be used for live production.
    """

    pass
