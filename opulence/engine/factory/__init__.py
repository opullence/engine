from opulence.common.configuration import load_config_from_file

from .factory import Factory

load_config_from_file()
factory = Factory()
factory.setup()
