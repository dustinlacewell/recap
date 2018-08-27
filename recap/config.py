import os
from pathlib import Path as P
from shutil import copyfile


import toml
from attrdict import AttrDict as A

from recap.merge import dict_merge


CONF_NAME = "rc.toml"

XDG_CONFIG_HOME = P(os.getenv(
    "XDG_CONFIG_HOME", os.path.expandvars(os.path.join("$HOME", ".config"))))

CONFIG_HOME = XDG_CONFIG_HOME / "recap"


class RecapConfig:

    def __init__(self, config_path):
        self.package_path = P(__file__).parent
        self.data_path = self.package_path / "data"
        self.config_path = P(config_path)

        self.ensure_config_path()
        self.ensure_config_file()

        self.defaults = toml.load(str(self.data_path / CONF_NAME))
        self.user_rc = toml.load(str(self.config_path / CONF_NAME))
        self.rc = A(dict_merge(self.defaults, self.user_rc))

    def ensure_config_path(self):
        self.config_path.mkdir(parents=True, exist_ok=True)

    def ensure_config_file(self):
        src = self.data_path / CONF_NAME
        dst = self.config_path / CONF_NAME
        if not dst.exists():
            copyfile(src, dst)


rc = RecapConfig(os.getenv('RECAP_CONFIG_HOME', CONFIG_HOME)).rc
