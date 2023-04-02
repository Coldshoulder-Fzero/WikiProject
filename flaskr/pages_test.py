from flaskr import create_app
from unittest.mock import patch
from io import BytesIO
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to the wiki" in resp.data

def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Pages" in resp.data

def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data

def test_sega_page(client):
    resp = client.get("pages/Sega")
    assert resp.status_code == 200
    assert b"Sega" in resp.data

def test_atari_page(client):
    resp = client.get("pages/Atari")
    assert resp.status_code == 200
    assert b"Atari" in resp.data

def test_ds_page(client):
    resp = client.get("pages/DS")
    assert resp.status_code == 200
    assert b"DS" in resp.data

def test_mobile_gaming_page(client):
    resp = client.get("pages/Mobile Gaming")
    assert resp.status_code == 200
    assert b"Mobile Gaming" in resp.data

def test_nintendo_page(client):
    resp = client.get("pages/Nintendo")
    assert resp.status_code == 200
    assert b"Nintendo" in resp.data

def test_playstation_page(client):
    resp = client.get("pages/Playstation")
    assert resp.status_code == 200
    assert b"Playstation" in resp.data

def test_steam_page(client):
    resp = client.get("pages/Steam")
    assert resp.status_code == 200
    assert b"Steam" in resp.data

def test_tetris_page(client):
    resp = client.get("pages/Tetris")
    assert resp.status_code == 200
    assert b"Tetris" in resp.data

def test_wii_page(client):
    resp = client.get("pages/Wii")
    assert resp.status_code == 200
    assert b"Wii" in resp.data

def test_xbox_page(client):
    resp = client.get("pages/Xbox")
    assert resp.status_code == 200
    assert b"Xbox" in resp.data

def test_nonexistent_page(client):
    resp = client.get("pages/nonexistent")
    assert resp.status_code == 200
    assert b"No page exists with the given name:" in resp.data

def test_all_pages(client):
    sample_pages = ["test.txt", "info.txt"]
    with patch("flaskr.backend.Backend.get_all_page_names", return_value=sample_pages):
        resp = client.get("/pages")
        assert resp.status_code == 200
        assert b"Pages in the Wiki" in resp.data
 
@patch("flaskr.backend.Backend.get_wiki_page", return_value=b"Some info.")
def test_get_page(mock_get_wiki_page, client):
    name = "myimportantinfo"
    resp = client.get("/pages/myimportantinfo")
    assert resp.status_code == 200
    assert b"myimportantinfo" in resp.data
    assert b"Some info." in resp.data
    mock_get_wiki_page.assert_called_once_with(name)
 
@patch("flaskr.backend.Backend.get_image", return_value=BytesIO())
def test_get_image(mock_get_image, client):
   image_name = "my-image"
   resp = client.get("/images/my-image")
   assert resp.status_code == 200
   mock_get_image.assert_called_once_with(image_name)
