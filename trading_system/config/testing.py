import utils
from .general import GeneralConfig


class TestingConfig(GeneralConfig):
    """
    This configuration will be used for testing purposes, including unit tests.
    """

    base_dir = utils.join_paths(utils.BASE_DIR, 'tests')
    TESTING = True
    SYMBOLS = ['BTC', 'ETH', 'LTC']
