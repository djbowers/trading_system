from .general import GeneralConfig


class DevelopmentConfig(GeneralConfig):
    """
    This configuration is for development environments. It enables debugging and
    potential future features for developers.
    """

    DEBUG = True
