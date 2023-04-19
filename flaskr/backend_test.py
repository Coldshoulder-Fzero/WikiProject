from flaskr.backend import Backend
from unittest.mock import MagicMock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest
"""
This fixture just creates a mock object that we will use to represent the
filestream used in our blobs.
"""


@pytest.fixture
def file_stream():
    return MagicMock()


"""
To read/write to blobs, we will need to call blob.open(). This fixture sets the
filestream for our blob.open() function call so we can control what is read/
written.

The fixture returns a blob that will interact with the given filestream.
"""


@pytest.fixture
def blob(file_stream):
    blob = MagicMock()
    blob.open.return_value.__enter__.return_value = file_stream
    return blob


"""
This helper method creates a mocked Bucket object. It takes in a mocked blob
object which we will use as the return value for methods called on the bucket. 
Any call to get_blob() or blob() will return the mocked blob object.
"""


def make_bucket(blob):
    bucket = MagicMock()
    bucket.get_blob.return_value = blob
    bucket.blob.return_value = blob
    return bucket


"""
This fixture helps use mock the sha256 object that we use when we hash our 
username and password. It specifically mocks the hexdigest() function call and 
sets the return value as return_value.
"""


def sha256(return_value):
    hash_object = MagicMock()
    hash_object.hexdigest.return_value = return_value
    return hash_object


"""
This fixture helps us mock the content bucket used to store the page contents. 
It uses the make_bucket() helper method that we defined above.
"""


@pytest.fixture
def content_bucket(blob):
    return make_bucket(blob)


"""
This fixture helps us mock the user bucket used to store the page contents. It 
uses the make_bucket() helper method that we defined above.
"""


@pytest.fixture
def user_bucket(blob):
    return make_bucket(blob)


"""
This fixture helps us mock the Backend class. We will mock the storage client 
and set the two buckets to the mocked bucket objects we created in the fixtures 
above. 
"""


@pytest.fixture
def backend(user_bucket, content_bucket):
    storage_client = MagicMock()
    storage_client.bucket = MagicMock()
    """
    So in Backend, we make two calls to storage_client.bucket() to create the 
    buckets. We want the first call to return the mock user bucket and the 
    second call to return the mock content bucket. By setting the side_effect 
    to be a list, each call to storage_client.bucket() will return the next 
    mocked object in the list.
    """
    storage_client.bucket.side_effect = [user_bucket, content_bucket]
    return Backend(storage_client=storage_client)


def test_get_wiki_page_success(backend, content_bucket, file_stream):
    file_stream.read.return_value = "test worked"

    value = backend.get_wiki_page("test")

    content_bucket.get_blob.assert_called_with("test")
    assert value == "test worked"


def test_get_wiki_page_failure(backend, content_bucket):
    content_bucket.get_blob.return_value = None
    try:
        backend.get_wiki_page("test")
    except ValueError as ve:
        assert str(ve) == "No page exists with the given name: test"


def test_get_all_pages(backend, content_bucket):
    blobs = [MagicMock() for _ in range(5)]
    blobs[0].name = "test0"
    blobs[1].name = "test1.png"
    blobs[2].name = "test2.jpg"
    blobs[3].name = "test3"
    blobs[4].name = "test4.jpeg"
    content_bucket.list_blobs.return_value = blobs

    value = backend.get_all_page_names()

    content_bucket.list_blobs.assert_called_with()
    assert value == ["test0", "test3"]


def test_upload_success(backend, content_bucket, blob, file_stream):
    content_bucket.get_blob.return_value = None

    backend.upload("test", "test data")

    content_bucket.blob.assert_called_with("test")
    blob.open.assert_called_with("wb")
    file_stream.write.assert_called_with("test data")


def test_upload_failure(backend, content_bucket):
    try:
        backend.upload("test", "test data")
    except ValueError as v:
        assert str(v) == "test already exists in the content bucket!"

    content_bucket.get_blob.assert_called_with("test")


def test_get_image_success(backend, content_bucket, blob, file_stream):
    file_stream.read.return_value = "test data".encode()

    image = backend.get_image("test")

    content_bucket.get_blob.assert_called_with("test")
    blob.open.assert_called_with("rb")
    assert image.read() == "test data".encode()


def test_get_image_failure(backend, content_bucket):
    content_bucket.get_blob.return_value = None

    image = backend.get_image("test")

    assert image.read() == "".encode()


@patch('flaskr.backend.sha256', return_value=sha256("test hash"))
def test_sign_up_success(hash, backend, user_bucket, blob, file_stream):
    user_bucket.get_blob.return_value = None

    user = backend.sign_up("test_user", "password")

    user_bucket.blob.assert_called_with("test_user")
    blob.open.assert_called_with("w")
    hash.assert_called_with("test_user:password".encode())
    file_stream.write.assert_called_with("test hash")

    assert user.username == "test_user"


def test_sign_up_failure(backend, user_bucket, blob, file_stream):
    try:
        backend.sign_up("test_user", "password")
    except ValueError as v:
        assert str(v) == "Username test_user already exists!"

    user_bucket.get_blob.assert_called_with("test_user")


@patch('flaskr.backend.sha256', return_value=sha256("test hash"))
def test_sign_in_success(hash, backend, user_bucket, blob, file_stream):
    file_stream.read.return_value = "test hash"

    user = backend.sign_in("test_user", "password")

    user_bucket.get_blob.assert_called_with("test_user")
    blob.open.assert_called_with()
    hash.assert_called_with("test_user:password".encode())
    assert user.username == "test_user"


def test_sign_in_no_user(backend, user_bucket, blob, file_stream):
    user_bucket.get_blob.return_value = None

    try:
        backend.sign_in("test_user", "password")
    except ValueError as v:
        assert str(v) == "Username test_user does not exist!"

    user_bucket.get_blob.assert_called_with("test_user")


@patch('flaskr.backend.sha256', return_value=sha256("bad hash"))
def test_sign_in_bad_password(hash, backend, user_bucket, blob, file_stream):
    file_stream.read.return_value = "test hash"

    try:
        backend.sign_in("test_user", "bad password")
    except ValueError as v:
        assert str(v) == "Invalid password for username test_user!"

    user_bucket.get_blob.assert_called_with("test_user")
    blob.open.assert_called_with()
    hash.assert_called_with("test_user:bad password".encode())

def test_save_wiki_page_new(backend, content_bucket, blob, file_stream):
    content_bucket.blob.return_value.exists.return_value = False
    content_bucket.get_blob.return_value = blob

    backend.save_wiki_page("test", "test content", "test_user")

    content_bucket.blob.assert_called_with("test")
    blob.upload_from_string.assert_called_with("test content")


def test_save_wiki_page_existing(backend, content_bucket, blob, file_stream):
    content_bucket.blob.return_value.exists.return_value = True
    file_stream.read.return_value = "existing content"

    backend.save_wiki_page("test", "new content", "test_user")

    content_bucket.blob.assert_called_with("history/test-")
    blob.upload_from_string.assert_called_with("existing content")
    content_bucket.blob.assert_called_with("test")
    blob.upload_from_string.assert_called_with("new content")


def test_get_previous_version(backend, content_bucket, blob):
    history_blobs = [MagicMock() for _ in range(3)]
    for i, b in enumerate(history_blobs):
        b.name = f"history/test-{i}"
        b.download_as_text.return_value = f"version {i}"
    content_bucket.list_blobs.return_value = history_blobs

    content, timestamp, username = backend.get_previous_version("test")

    content_bucket.list_blobs.assert_called_with(prefix='history/test')
    assert content == "version 2"
    assert timestamp is not None
    assert username == "test_user"


def test_revert_to_previous_success(backend, content_bucket, blob):
    history_blobs = [MagicMock() for _ in range(3)]
    for i, b in enumerate(history_blobs):
        b.name = f"history/test-{i}"
        b.download_as_text.return_value = f"version {i}"
    content_bucket.list_blobs.return_value = history_blobs

    result = backend.revert_to_previous("test", "test_user")

    assert result is True


def test_revert_to_previous_failure(backend, content_bucket, blob):
    content_bucket.list_blobs.return_value = []

    result = backend.revert_to_previous("test", "test_user")

    assert result is False


def test_get_all_previous_versions(backend, content_bucket, blob):
    history_blobs = [MagicMock() for _ in range(5)]
    for i, b in enumerate(history_blobs):
        b.name = f"history/test-{i}-test_user.txt"
    content_bucket.list_blobs.return_value = history_blobs

    versions = backend.get_all_previous_versions("test")

    content_bucket.list_blobs.assert_called_with(prefix="history/test")
    assert len(versions) == 5
    for i, (name, timestamp, username) in enumerate(versions):
        assert name == f"history/test-{i}-test_user.txt"
        assert timestamp is not None
        assert username == "test_user"