from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import delete_dir


def get_temp_dir():
    return "src/ch14_moment/test/_util/moment_mstr"


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
