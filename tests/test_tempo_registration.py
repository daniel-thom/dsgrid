import getpass
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from dsgrid.registry.registry_manager import RegistryManager
from dsgrid.tests.common import (
    create_local_test_registry,
    make_standard_scenarios_project_dir,
    TEST_DATASET_DIRECTORY,
)
from dsgrid.utils.files import dump_data, load_data
from dsgrid.tests.common import (
    replace_dimension_uuids_from_registry,
)


logger = logging.getLogger()


def test_register_project_and_dataset(make_standard_scenarios_project_dir):
    with TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        manager = make_registry_for_tempo(
            base_dir, make_standard_scenarios_project_dir, TEST_DATASET_DIRECTORY
        )
        # TODO: not working yet
        # dataset_mgr = manager.dataset_manager
        # config_ids = dataset_mgr.list_ids()
        # assert len(config_ids) == 1
        # assert config_ids[0] == "tempo_standard_scenarios_2021"


def make_registry_for_tempo(registry_path, src_dir, dataset_path=None) -> RegistryManager:
    """Creates a local registry to test registration of TEMPO dimensions and dataset.

    Parameters
    ----------
    registry_path : Path
        Path in which the registry will be created.
    src_dir : Path
        Path containing source config files
    dataset_path : Path | None
        If None, use "DSGRID_LOCAL_DATA_DIRECTORY" env variable.

    """
    if dataset_path is None:
        dataset_path = os.environ["DSGRID_LOCAL_DATA_DIRECTORY"]
    path = create_local_test_registry(registry_path)
    dataset_dir = Path("datasets/sector_models/tempo_standard_scenarios_2021")
    user = getpass.getuser()
    log_message = "Initial registration"
    manager = RegistryManager.load(path, offline_mode=True)
    dim_mgr = manager.dimension_manager
    dim_mgr.register(src_dir / dataset_dir / "dimensions.toml", user, log_message)

    # TODO: register a project and submit the dataset.
    # For now, only test the dataset.
    # project_config_file = src_dir / "project.toml"
    # project_id = load_data(project_config_file)["project_id"]
    dataset_config_file = src_dir / dataset_dir / "dataset.toml"
    dataset_id = load_data(dataset_config_file)["dataset_id"]
    replace_dataset_path(dataset_config_file, dataset_path=dataset_path)
    # replace_dimension_uuids_from_registry(path, (project_config_file, dataset_config_file))
    replace_dimension_uuids_from_registry(path, (dataset_config_file,))

    # TODO: this fails because we don't have a complete set of TEMPO data tables.
    # manager.dataset_manager.register(dataset_config_file, user, log_message)
    # manager.project_manager.register(project_config_file, user, log_message)
    # manager.project_manager.submit_dataset(
    #    project_id,
    #    dataset_id,
    #    [],
    #    user,
    #    log_message,
    # )
    return manager


def replace_dataset_path(dataset_config_file, dataset_path):
    config = load_data(dataset_config_file)
    src_data = Path(dataset_path) / config["dataset_id"]
    config["path"] = str(src_data)
    dump_data(config, dataset_config_file)
    logger.info("Replaced dataset path in %s with %s", dataset_config_file, src_data)
