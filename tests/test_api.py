import pytest

HEADERS = {"X-API-KEY": "test-secret-key", "Content-Type": "application/json"}
BAD_HEADERS = {"X-API-KEY": "wrongkey", "Content-Type": "application/json"}


class TestAuthentication:
    def test_missing_api_key_returns_401(self, client):
        res = client.post("/sum", json={"numbers": [1, 2, 3]})
        assert res.status_code == 401

    def test_wrong_api_key_returns_401(self, client):
        res = client.post("/sum", headers=BAD_HEADERS, json={"numbers": [1, 2]})
        assert res.status_code == 401

    def test_correct_key_is_accepted(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [1]})
        assert res.status_code == 200


class TestSumEndpoint:
    def test_basic_sequential_sum(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [5, 10, 15]})
        body = res.get_json()
        assert res.status_code == 200
        assert body["result"] == 30
        assert body["operations_performed"] == 3

    def test_negative_numbers(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [-5, 5]})
        assert res.get_json()["result"] == 0

    def test_floats(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [1.5, 2.5]})
        assert res.get_json()["result"] == pytest.approx(4.0)

    def test_single_element(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [42]})
        assert res.get_json()["result"] == 42

    def test_missing_numbers_key_returns_400(self, client):
        res = client.post("/sum", headers=HEADERS, json={"data": [1, 2]})
        assert res.status_code == 400

    def test_empty_list_returns_422(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": []})
        assert res.status_code == 422

    def test_non_numeric_items_returns_422(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [1, "two", 3]})
        assert res.status_code == 422

    def test_numbers_not_a_list_returns_422(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": 42})
        assert res.status_code == 422

    def test_funny_message_is_present(self, client):
        res = client.post("/sum", headers=HEADERS, json={"numbers": [1, 2]})
        assert "message" in res.get_json()


class TestHealthCheck:
    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.get_json()["status"] == "ok"