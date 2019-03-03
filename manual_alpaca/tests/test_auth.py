# Standard library imports
import os

# Third party imports
import pytest

# Local application imports
from ..manual_alpaca import authenticate

# TODO: Learn how to encrypt keys for TravisCI
#@pytest.mark.skip(reason="Not sure yet how to encrypt API keys in tests")
@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_env_valid(mode):
    authenticate(mode=mode)


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_env_invalid(mode):
    os.environ["APCA_API_KEY_ID"] = "FAKE_PUBLIC_KEY"
    os.environ["APCA_API_SECRET_KEY"] = "FAKE_PRIVATE_KEY"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 2


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_env_empty(mode):
    os.environ["APCA_API_KEY_ID"] = ""
    os.environ["APCA_API_SECRET_KEY"] = ""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 1


# Will need to see if these can be encrypted/decrypted, not sure if possible.
@pytest.mark.skip(reason="Not sure yet how to encrypt API keys in tests")
@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_file_valid(mode):
    this_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_path, "..", "..", "config")
    secret_path = os.path.join(config_path, "secrets.yaml")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(auth_path=secret_path, mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 2


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_file_invalid(mode):
    this_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_path, "..", "..", "config")
    secret_path = os.path.join(config_path, "test_files", "fake-secrets.yaml")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(auth_path=secret_path, mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 2


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_file_empty(mode):
    this_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_path, "..", "..", "config")
    secret_path = os.path.join(config_path, "test_files", "empty-secrets.yaml")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(auth_path=secret_path, mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 2


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_file_no_yaml_keys(mode):
    this_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_path, "..", "..", "config")
    secret_path = os.path.join(config_path, "test_files", "no-secrets.yaml")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(auth_path=secret_path, mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 1


@pytest.mark.parametrize("mode", ["live", "paper"])
def test_auth_from_file_not_yaml(mode):
    this_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_path, "..", "..", "config")
    secret_path = os.path.join(config_path, "test_files", "not-yaml.txt")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        authenticate(auth_path=secret_path, mode=mode)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.type == 3
