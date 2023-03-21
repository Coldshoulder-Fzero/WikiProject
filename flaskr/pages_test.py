from flaskr import create_app


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


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<title>awesomeWikiViewer</title>" in resp.data
    assert b"<h3>Welcome to the wiki!</h3>" in resp.data


def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Pages" in resp.data

def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data

def test_sega_page(client):
    resp = client.get("/sega")
    assert resp.status_code == 200
    assert b"Sega" in resp.data

def test_atari_page(client):
    resp = client.get("/Atari")
    assert resp.status_code == 200
    assert b"Atari" in resp.data

def test_ds_page(client):
    resp = client.get("/DS")
    assert resp.status_code == 200
    assert b"DS" in resp.data

def test_mobile_gaming_page(client):
    resp = client.get("/MobileGaming")
    assert resp.status_code == 200
    assert b"MobileGaming" in resp.data

def test_nintendo_page(client):
    resp = client.get("/Nintendo")
    assert resp.status_code == 200
    assert b"Nintendo" in resp.data

def test_playstation_page(client):
    resp = client.get("/Playstation")
    assert resp.status_code == 200
    assert b"Playstation" in resp.data

def test_steam_page(client):
    resp = client.get("/Steam")
    assert resp.status_code == 200
    assert b"Steam" in resp.data

def test_tetris_page(client):
    resp = client.get("/Tetris")
    assert resp.status_code == 200
    assert b"Tetris" in resp.data

def test_wii_page(client):
    resp = client.get("/Wii")
    assert resp.status_code == 200
    assert b"Wii" in resp.data

def test_xbox_page(client):
    resp = client.get("/xbox")
    assert resp.status_code == 200
    assert b"Xbox" in resp.data

def test_nonexistent_page(client):
    resp = client.get("/nonexistent")
    assert resp.status_code == 404