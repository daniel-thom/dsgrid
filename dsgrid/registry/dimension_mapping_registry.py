import logging
from pathlib import Path


from .registry_base import RegistryBaseModel, RegistryBase
from dsgrid.filesystem.factory import make_filesystem_interface
from dsgrid.common import REMOTE_REGISTRY

logger = logging.getLogger(__name__)


class DimensionMappingRegistry(RegistryBase):
    """Controls registration for dimension mappings"""

    DIMENSION_MAPPING_REGISTRY_PATH = Path("configs/dimension_mappings")

    @staticmethod
    def config_filename():
        return "dimension_mapping.toml"

    @staticmethod
    def model_class():
        return RegistryBaseModel

    @staticmethod
    def registry_path():
        return DimensionMappingRegistry.DIMENSION_MAPPING_REGISTRY_PATH
