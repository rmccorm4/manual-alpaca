# Standard library imports
import os

# Third party imports
import pytest

# Local application imports
from ..manual_alpaca import authenticate

# TODO: Learn how to encrypt keys for TravisCI
# Export real keys before testing
@pytest.mark.skip(reason="Not sure yet how to encrypt API keys in tests")
def test_auth_from_env_valid():
    authenticate(mode="paper")


def test_auth_from_env_invalid():
    os.environ["APCA_API_KEY_ID"] = "FAKE_PUBLIC_KEY"
    os.environ["APCA_API_SECRET_KEY"] = "FAKE_PRIVATE_KEY"
    authenticate(mode="paper")

    os.environ["APCA_API_KEY_ID"] = "FAKE_PUBLIC_KEY"
    os.environ["APCA_API_SECRET_KEY"] = "FAKE_PRIVATE_KEY"
    authenticate(mode="paper")


# Will need to see if these can be encrypted/decrypted, not sure if possible.
@pytest.mark.skip(reason="Not sure yet how to encrypt API keys in tests")
def test_auth_from_file_valid():
    authenticate(auth_path="config/secrets.yaml", mode="paper")
    authenticate(auth_path="config/secrets.yaml", mode="live")


def test_auth_from_file_invalid():
    authenticate(auth_path="config/fake-secrets.yaml", mode="paper")
    authenticate(auth_path="config/fake-secrets.yaml", mode="live")
