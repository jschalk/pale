from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import create_path, delete_dir


def src_chapter_dir() -> str:
    # return "src/ch17_idea"
    return create_path("src", "ch17_idea")


def get_temp_dir() -> str:
    # return "src/ch17_idea/test/_util/idea_examples"
    test_dir = create_path(src_chapter_dir(), "test")
    _util_dir = create_path(test_dir, "_util")
    return create_path(_util_dir, "idea_examples")


def idea_moment_mstr_dir() -> str:
    return create_path(get_temp_dir(), "moment_mstr")


def idea_moments_dir() -> str:
    return create_path(idea_moment_mstr_dir(), "moments")
    # return "src/ch17_idea/test/_util/idea_examples/moment_mstr/moments"


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
