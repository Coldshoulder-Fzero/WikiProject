from flaskr import create_app, user, backend
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
import pytest


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'LOGIN_DISABLED': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Upload to the Wiki" in resp.data


# Here, we are using parameters to run the same unit test but with different
# inputs. We will test all the different ways for upload to fail.
@pytest.mark.parametrize(('wikiname', 'wikicontent'), (
    ('', {}),
    ('my-data', {}),
    ('my-data', {'filename', None}),
))
def test_unable_to_upload(client, wikiname, wikicontent):
    resp = client.post("/upload",
                       data={
                           "wikiname": wikiname,
                           "wikicontent": wikicontent
                       })
    assert resp.status_code == 200
    assert b"Unable to Upload" in resp.data


@patch('flaskr.backend.Backend.upload', autospec=True)
def test_upload_failed(mock_upload, client):
    # side_effect allows use to raise exceptions when mocking
    # https://docs.python.org/3/library/unittest.mock.html#quick-guide
    mock_upload.side_effect = ValueError("myfile.txt already exists")

    # we use FileStorage object to represent the file we're uploading.
    # https://werkzeug.palletsprojects.com/en/2.2.x/datastructures/#werkzeug.datastructures.FileStorage
    resp = client.post("/upload",
                       data={
                           "wikiname": "mywikiname",
                           "wikicontent": FileStorage(filename="myfile.txt")
                       })
    assert resp.status_code == 200
    assert b"Upload Failed!" in resp.data


def test_upload_successful(client):
    # mock the backend upload() method to make things easier. We do not have to
    # mock the buckets or blobs.
    with patch('flaskr.backend.Backend.upload', return_value=None):
        # mock the get_wiki_page() method which is called when we redirect the
        # user after uploading the page.
        with patch("flaskr.backend.Backend.get_wiki_page",
                   return_value=b"Some info."):
            upload_resp = client.post("/upload",
                                      data={
                                          "wikiname":
                                              "mywikiname",
                                          "wikicontent":
                                              FileStorage(filename="myfile.txt",
                                                          stream=b"Some info.")
                                      })
            assert upload_resp.status_code == 200
            pages_resp = client.get("/pages/mywikiname")
            assert pages_resp.status_code == 200
            assert b"mywikiname" in pages_resp.data
            assert b"Some info." in pages_resp.data
