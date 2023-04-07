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

'''
This fixture will mock the admin bucket. It is using make_bucket method for creating a mocked bucket object
'''

@pytest.fixture
def admin_bucket(blob):
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
    storage_client.bucket.side_effect = [user_bucket, content_bucket, admin_bucket]
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

'''
Will mock an admin test by passing another hashed password. 
First method tests for a successfull admin log in
Second method tests for unsuccessfull admin log in
'''
@patch('flaskr.backend.sha256', return_value=sha256("admin hash"))
def test_sign_in_admin_success(hash, backend, admin_bucket, blob, file_stream):
    file_stream.read.return_value= "admin hash"

    admin = backend.sign_in("admin_user", "testing123")

    admin_bucket.get_blob.assert_called_with("admin_user")
    blob.open.assert_called_with()
    hash.assert_called_with("admin_user:testing123".encode())
    assert admin.username == "admin_user"

@patch('flask.backend.sha256', return_value=sha256("user hash"))
def test_sign_in_admin_fail(hash, backend,admin_bucket, blob, filestream):
    file_stream.read.return_value = "admin hash"
    try:
        backend.sign_in("admin_user", "user123")
    except ValueError as v:
        assert str(v) == "Invadid password for username admin_user!"
    
    admin_bucket.get_blob.assert_called_with("admin_user")
    blob.open.assert_called_with()
    hash.assert_called_with("admin_user:user123".encode())

