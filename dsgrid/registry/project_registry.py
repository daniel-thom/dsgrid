"""Manages the registry for a project."""

import logging
from pathlib import Path
from typing import List, Optional, Union

from pydantic import Field
from pydantic import validator
from semver import VersionInfo

from .registry_base import RegistryBaseModel, RegistryBase
from dsgrid.data_models import DSGBaseModel
from dsgrid.registry.common import (
    DatasetRegistryStatus,
    ProjectRegistryStatus,
)
from dsgrid.utils.versioning import make_version

logger = logging.getLogger(__name__)


class ProjectDatasetRegistryModel(DSGBaseModel):
    """Project registration details for datasets"""

    dataset_id: str = Field(
        title="dataset_id",
        description="dataset identifier",
    )
    version: Optional[Union[None, str, VersionInfo]] = Field(
        title="dataset_version",
        description="full dataset version to be used to find dataset registry",
    )
    status: DatasetRegistryStatus = Field(
        title="status",
        description="dataset status within the project",
    )

    @validator("version")
    def check_version(cls, version):
        if isinstance(version, VersionInfo) or version is None:
            return version
        return make_version(version)


class ProjectRegistryModel(RegistryBaseModel):
    """Defines project registry"""

    project_id: str = Field(
        tile="project_id",
        description="unique project identifier",
    )
    status: ProjectRegistryStatus = Field(
        tile="status", description="project registry status", default="Initial Registration"
    )
    dataset_registries: Optional[List[ProjectDatasetRegistryModel]] = Field(
        title="dataset_registries",
        description="list of dataset registry",
    )


class ProjectRegistry(RegistryBase):
    """Controls a project registry."""

    PROJECT_REGISTRY_PATH = Path("configs/projects")

    @staticmethod
    def config_filename():
        return "project.toml"

    @staticmethod
    def model_class():
        return ProjectRegistryModel

    @staticmethod
    def registry_path():
        return ProjectRegistry.PROJECT_REGISTRY_PATH

    def has_dataset(self, dataset_id, status):
        """Return True if the dataset_id is stored with status."""
        for registry in self._model.dataset_registries:
            if registry.dataset_id == dataset_id:
                return registry.status == status
        return False

    def set_dataset_status(self, dataset_id, status):
        """Set the dataset status to the given value.

        Parameters
        ----------
        dataset_id : str
        status : DatasetRegistryStatus

        Raises
        ------
        ValueError
            Raised if dataset_id is not stored.

        """
        for registry in self._model.dataset_registries:
            if registry.dataset_id == dataset_id:
                registry.status = status
                logger.info(
                    "Set dataset_id=%s status=%s for project=%s",
                    dataset_id,
                    status,
                    self.project_id,
                )
                return

        raise ValueError(f"dataset_id={dataset_id} is not stored.")

    @property
    def project_id(self):
        return self._model.project_id

    def list_registered_datasets(self):
        """Get registered datasets associated with project registry.

        Returns
        -------
        list
            list of dataset IDs

        """
        status = DatasetRegistryStatus.REGISTERED
        return [x.dataset_id for x in self._iter_datasets_by_status(status)]

    def list_unregistered_datasets(self):
        """Get unregistered datasets associated with project registry.

        Returns
        -------
        list
            list of dataset IDs

        """
        status = DatasetRegistryStatus.UNREGISTERED
        return [x.dataset_id for x in self._iter_datasets_by_status(status)]

    def _iter_datasets_by_status(self, status):
        for registry in self._model.dataset_registries:
            if registry.status == status:
                yield registry

    @property
    def project_config(self):
        """Return the ProjectConfig."""
        return self._model.project_config
