import os
import shutil
from code import InteractiveInterpreter
from ConfigParser import RawConfigParser
from django.core.management.base import BaseCommand, CommandError
from .create_local import (CommonMixin,
                           CONFIG_DIR_NAME,
                           DEFAULT_CONFIG_NAME)

CODE = """
from ConfigParser import RawConfigParser
import os

def get_config():
    root = os.path.dirname(__file__)
    path = os.path.join(root, 'configs',
                        "%s_%s.cfg" % (os.uname()[1], os.getenv('USERNAME') or 'nouser'))
    if not os.path.exists(path):
        path = os.path.join(root,
                            'configs',
                            "default.cfg")
    config = RawConfigParser()
    config.read(path)
    return config
config = get_config()

DEBUG = config.get('debug','DEBUG')
TEMPLATE_DEBUG = config.get('debug','TEMPLATE_DEBUG')
db_attrs = ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']

DATABASES = {
    'default' : dict([(x, config.get('database', x))
                      for x in db_attrs])
}
"""

class Command(BaseCommand, CommonMixin):

    def _check_configs(self):
        if (os.path.exists(self.configs_path) and
            os.path.exists(self.default_config_path)):
            raise CommandError("Looks like this project is already using local configs, aborting")


    def handle(self, *args, **options):
        self._initialize_paths()
        self._check_settings()
        self._check_configs()
        settings = open(self.settings_path, 'r')
        db_braces = 0
        db_lines = []
        other_lines = []
        debug_line, template_debug_line = None, None
        for line in settings:
            if line.startswith('DEBUG'):
                debug_line = line
            elif line.startswith('TEMPLATE_DEBUG'):
                template_debug_line = line
            elif line.startswith('DATABASES') and '{' in line:
                db_braces = 1
                db_lines.append(line)
            elif db_braces:
                db_lines.append(line)
                if '{' in line:
                    db_braces += 1
                elif '}' in line:
                    db_braces -= 1
            else:
                other_lines.append(line)

        with open(os.path.join(self.base, 'new_settings.py'), 'w') as new_settings:
            new_settings.write(CODE)
            new_settings.write(''.join(other_lines))
        context = InteractiveInterpreter()
        context.runcode(''.join(db_lines))
        if debug_line: context.runcode(debug_line)
        if template_debug_line: context.runcode(template_debug_line)
        if not os.path.exists(self.configs_path):
            os.mkdir(self.configs_path)
        config = RawConfigParser()
        config.add_section('debug')
        config.set('debug', 'DEBUG', context.locals['DEBUG'])
        config.set('debug', 'TEMPLATE_DEBUG', context.locals['TEMPLATE_DEBUG'])
        db_attrs = ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']
        config.add_section('database')
        for x in db_attrs:
            config.set('database', x, context.locals['DATABASES']['default'][x])
        with open(self.default_config_path, 'w') as config_file:
            config.write(config_file)
