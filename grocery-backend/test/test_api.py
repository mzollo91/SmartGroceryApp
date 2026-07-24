"""Script to test API functions with pytest."""
import math

def test_fixture_chain_runs(client):
    assert True

def test_valid_aisles(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 2})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] == 5.0
    assert response.json()["path"] == [1,2] # Even though it's clear from the seed data that a distance of 5.0 can only be achieved form a path of 1->2, it's still best practice to validate the entire output.

def test_missing_aisle_ids(client):
    response = client.get(url="/api/route", params={"start_id":20,
                                                    "end_id": 21})
    assert response.status_code == 404
    assert response.json()["detail"][0] == 20
    assert response.json()["detail"][1] == 21

def test_no_valid_path(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 4})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] is None
    assert response.json()["path"] == []

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
    assert response.json()["path"] == [1]

def test_shortest_path(client):
    response = client.get(url="/api/route", params={"start_id":1,
                                                    "end_id": 5})
    assert response.status_code == 200
    assert response.json()["totalDistanceFeet"] == 2.0
    assert response.json()["path"] == [1,3,5] # 2 Valid paths exist; 1->2->5 with a distance of 8.0, and 1->3->5 with a distance of 2.0.