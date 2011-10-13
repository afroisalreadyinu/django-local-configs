django_local_configs helps you work on a project on different
computers and as different users by making certain configuration
options dependent on computer name and user name. Two commands added
to manage.py can be used to move config options which are different on
various development environments to a directory in the base of a
django project. These options are then read into the settings.py
file. This is something I did with every django prokect anyway, so I
decided to moved it to a module of its own.

Quick howto: Add django_local_configs to your installed apps, run the
command './manage.py localize_settings' in the project root, then run
'./manage.py create_local_config' each time you're in a new
environment. This second command will create a copy of a default
config, already populated with the values in settings.py when you ran
the first command.

localize_settings, when run from a directory in which there is a
settings.py file, does two things. It modifies the contents of the
settings.py file, removing the configs for database and debug and
adding small amount of code to the beginning which import the removed
stuff from a config. The new settings file is moved instead of the old
one, but the old is not deleted; it is renamed old_settings.py. The
second thing it does is to create a directory called configs, and add
a default config file named default.cfg. The configuration values
removed from settings.py are added into this config file.

create_local_config creates a new config file in the configs
directory. The name of this config file is based on the uname of the
computer and the user login name. If the computer is named comp, and
the user linuxuser, the config file is named comp_linuxuser.cfg. The
code added by the first command uses the same scheme to look for a
suitable config file to load when settings.py is loaded.
