from abc import ABCMeta

import utils


class GeneralConfig:
    """
    Base configuration class. Any configuration parameters that do not change
    between environments should be declared here as global class constants.
    """

    __metaclass__ = ABCMeta

    base_dir = utils.BASE_DIR

    @property
    def data_dir(self):
        return utils.join_paths(self.base_dir, 'data')

    @property
    def price_dir(self):
        return utils.join_paths(self.data_dir, 'price')
