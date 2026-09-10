from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from api.v1.enterprise import get_enterprise_service, get_manager_enterprise_service
from api.v1.vehicle import get_vehicle_service
from core.auth import get_current_user
from main import app


class FakeEnterpriseService:
    def __init__(self, enterprise=None, vehicles=(), drivers=()):
        self.enterprise = enterprise
        if self.enterprise is not None:
            self.enterprise.vehicles = list(vehicles)
            self.enterprise.drivers = list(drivers)

    async def get_by_id(self, enterprise_id):
        return self.enterprise

    async def update(self, **kwargs):
        return {"id": kwargs["id"]}

    async def delete_by_id(self, **kwargs):
        return None

    async def create(self, **kwargs):
        return {"name": kwargs["name"], "city": kwargs["city"]}


class FakeVehicleService:
    def __init__(self, vehicle=None):
        self.vehicle = vehicle

    async def get_by_id(self, vehicle_id):
        return self.vehicle


class FakeManagerEnterpriseService:
    def __init__(self, enterprise_ids=(), enterprise_manager_ids=()):
        self.enterprise_ids = set(enterprise_ids)
        self.enterprise_manager_ids = set(enterprise_manager_ids)

    async def get_manager_enterprises(self, manager_id):
        return [SimpleNamespace(enterprise_id=enterprise_id) for enterprise_id in self.enterprise_ids]

    async def get_enterprise_managers(self, enterprise_id):
        return [SimpleNamespace(manager_id=manager_id) for manager_id in self.enterprise_manager_ids]


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def authenticated_user():
    return SimpleNamespace(id=1)


def override_current_user():
    return authenticated_user()


def test_unauthenticated_requests_return_401(client):
    for method, url in (
        ("get", "/api/v1/enterprises/1"),
        ("put", "/api/v1/enterprises/1"),
        ("post", "/api/v1/enterprises/"),
        ("delete", "/api/v1/enterprises/1"),
    ):
        request = {"name": "Парк", "city": "Москва"}
        response = client.request(method.upper(), url, json=request)
        assert response.status_code == 401


def test_invalid_credentials_return_401(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "test"},
    )

    assert response.status_code == 401


def test_invalid_request_returns_400(client):
    app.dependency_overrides[get_current_user] = override_current_user

    response = client.put("/api/v1/enterprises/1", content="not-json")

    assert response.status_code == 400


def test_invalid_field_values_return_422(client):
    app.dependency_overrides[get_current_user] = override_current_user

    response = client.put(
        "/api/v1/vehicles/1",
        json={
            "price": -1,
            "year": 2020,
            "mileage": 0,
            "number_of_owners": 0,
            "plate_number": "A123AA",
            "enterprise_id": 1,
        },
    )

    assert response.status_code == 422


def test_missing_enterprise_returns_404(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService()

    response = client.get("/api/v1/enterprises/999")

    assert response.status_code == 404


def test_missing_vehicle_returns_404(client):
    app.dependency_overrides[get_vehicle_service] = lambda: FakeVehicleService()

    response = client.get("/api/v1/vehicles/999")

    assert response.status_code == 404


def test_manager_without_enterprise_permissions_returns_403(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService(SimpleNamespace(id=1))
    app.dependency_overrides[get_manager_enterprise_service] = lambda: FakeManagerEnterpriseService()

    response = client.put("/api/v1/enterprises/1", json={"name": "Парк", "city": "Москва"})

    assert response.status_code == 403


def test_put_returns_200(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService(SimpleNamespace(id=1))
    app.dependency_overrides[get_manager_enterprise_service] = lambda: FakeManagerEnterpriseService({1})

    response = client.put("/api/v1/enterprises/1", json={"name": "Парк", "city": "Москва"})

    assert response.status_code == 200


def test_post_returns_201(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService()

    response = client.post("/api/v1/enterprises/", params={"name": "Парк", "city": "Москва"})

    assert response.status_code == 201


def test_delete_returns_204(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService(SimpleNamespace(id=1))
    app.dependency_overrides[get_manager_enterprise_service] = lambda: FakeManagerEnterpriseService({1})

    response = client.delete("/api/v1/enterprises/1")

    assert response.status_code == 204


def test_delete_enterprise_with_vehicles_returns_409(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService(
        SimpleNamespace(id=1), vehicles=[SimpleNamespace(id=10)]
    )
    app.dependency_overrides[get_manager_enterprise_service] = lambda: FakeManagerEnterpriseService({1}, {1})

    response = client.delete("/api/v1/enterprises/1")

    assert response.status_code == 409


def test_delete_enterprise_visible_to_other_manager_returns_409(client):
    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_enterprise_service] = lambda: FakeEnterpriseService(SimpleNamespace(id=1))
    app.dependency_overrides[get_manager_enterprise_service] = lambda: FakeManagerEnterpriseService({1}, {1, 2})

    response = client.delete("/api/v1/enterprises/1")

    assert response.status_code == 409
