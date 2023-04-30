from pathlib import Path

import pytest

from pydocstyle import Configuration, Convention, IllegalConfiguration, load_config


def test_default_config() -> None:
    config = Configuration()

    assert config.convention == Convention.PEP257
    assert config.select == set()
    assert config.ignore == set()
    assert config.match != ""
    assert config.match_dir != ""
    assert config.ignore_decorators == None
    assert config.property_decorators == {
        "property",
        "cached_property",
        "functools.cached_property",
    }
    assert config.ignore_inline_noqa is False
    assert config.verbose is False


def test_load_config_returns_default_config_if_no_config_found(tmp_path: Path) -> None:
    assert load_config(tmp_path) == Configuration()


@pytest.mark.parametrize("config_file", ["ini_example.ini", "toml_example.toml"])
def test_loads_ini_and_toml_files_if_specified(config_file: str, resource_dir: Path) -> None:
    config = load_config(resource_dir / "configs" / config_file)

    assert config.convention == Convention.GOOGLE
    assert config.select == {"D100", "D200"}
    assert config.ignore == {"D100", "D300"}
    assert config.match == "abc"
    assert config.match_dir == "def"
    assert config.ignore_decorators == "[a-z].*"
    assert config.property_decorators == {"abc", "def"}
    assert config.ignore_inline_noqa is True
    assert config.verbose is True


@pytest.mark.parametrize("config_file", ["missing_section.ini", "missing_section.toml"])
def test_raises_error_if_configuration_is_missing_correct_section(
    config_file: str, resource_dir: Path
) -> None:
    with pytest.raises(IllegalConfiguration):
        load_config(resource_dir / "configs" / config_file)


@pytest.mark.parametrize("config_file", ["unknown_options.ini", "unknown_options.toml"])
def test_raises_error_if_unknown_options_are_present(config_file: str, resource_dir: Path) -> None:
    with pytest.raises(IllegalConfiguration):
        load_config(resource_dir / "configs" / config_file)


def test_raises_error_if_unparsable_file(tmp_path: Path) -> None:
    (tmp_path / "weird.bla").write_text("/([)")

    with pytest.raises(IllegalConfiguration):
        load_config(tmp_path / "weird.bla")


def test_discovery_in_same_folder(tmp_path: Path) -> None:
    (tmp_path / "setup.cfg").write_text("[pydocstyle]\nselect=D1\n")
    (tmp_path / "tox.ini").write_text("[pydocstyle]\nselect=D2\n")
    (tmp_path / "pyproject.toml").write_text('[tool.pydocstyle]\nselect="D3"\n')

    assert load_config(tmp_path).select == {"D1"}

    (tmp_path / "setup.cfg").unlink()

    assert load_config(tmp_path).select == {"D2"}

    (tmp_path / "tox.ini").unlink()

    assert load_config(tmp_path).select == {"D3"}
