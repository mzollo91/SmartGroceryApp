"""Script to test API functions with pytest."""
import math

def test_fixture_chain_runs(client):
    assert True

def test_valid_aisles(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 2})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] == 5.0

def test_missing_aisle_ids(client):
    response = client.get(url="/api/route", params={"start_id":7,
                                                    "end_id": 8})
    assert response.status_code == 404
    assert response.json()["detail"][0] == 7
    assert response.json()["detail"][1] == 8

def test_no_valid_path(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 3})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] is None

def test_different_stores(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 6})
    assert response.status_code == 400
    err_dict = response.json()["detail"]
    assert err_dict["1"] == 1
    assert err_dict["6"] == 2

def test_same_aisle(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 1})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] == 0.0

def test_shortest_path(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 4})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] == 8.0    