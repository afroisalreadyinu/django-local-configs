import os
from django.core.management.base import CommandError

CONFIG_DIR_NAME = 'configs'
DEFAULT_CONFIG_NAME = 'default.cfg'


class CommonMixin(object):

    def _check_settings(self):
        if not os.path.exists(self.settings_path):
            raise CommandError('Not executed from the base of a django project!')


    def _initialize_paths(self):
        self.base = os.getcwd()
        self.settings_path = os.path.join(self.base,
                                          'settings.py')
        self.configs_path = os.path.join(self.base,
                                         CONFIG_DIR_NAME)
        self.default_config_path = os.path.join(self.configs_path,
                                                DEFAULT_CONFIG_NAME)
