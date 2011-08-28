import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from . import CONFIG_DIR_NAME, DEFAULT_CONFIG_NAME, CommonMixin

class Command(BaseCommand, CommonMixin):

    can_import_settings = False

    def _config_name(self):
        username = os.getenv('USERNAME')
        if not username:
            username = 'www'
        comp_name = os.uname()[1]
        return "%s_%s.cfg" % (comp_name, username)


    def _is_config(self, filename):
        return filename.endswith('.cfg') and '_' in filename[:-4]


    def handle(self, *args, **options):
        self._initialize_paths()
        self._check_settings()
        config_name = self._config_name()
        file_path = os.path.join(self.configs_path, config_name)
        if not os.path.exists(self.configs_path):
            raise CommandError('Configs directory does not exist, please run localize_settings first')
        elif os.path.exists(file_path):
            raise CommandError('Local config %s already exists!' % config_name)

        existing_name = None
        if os.path.exists(self.default_config_path):
            existing_name = DEFAULT_CONFIG_NAME
        else:
            for f in os.listdir(configs_dir):
                if self._is_config(f):
                    existing_name = f
        if existing_name:
            shutil.copy(os.path.join(self.configs_path, existing_name), file_path)
            print 'Existing local config %s copied to %s' % (existing_name, config_name)
            return
        else:
            raise CommandError('There are no existing configs in the configs directory; please make sure that settings.py is valid, and run localize_settings.')
