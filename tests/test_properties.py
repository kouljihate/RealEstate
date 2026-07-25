import pytest
from httpx import AsyncClient


@pytest.fixture
async def auth_client(client: AsyncClient, clean_db):
    await client.post("/api/v1/auth/register", json={
        "email": "prop@test.com",
        "username": "propuser",
        "password": "TestPass123",
        "full_name": "Prop Owner",
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "prop@test.com",
        "password": "TestPass123",
    })
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.mark.asyncio
async def test_create_property(auth_client: AsyncClient):
    payload = {
        "title": "50 Hectare Organic Farm",
        "description": "Beautiful farmland with irrigation",
        "price": 250000.00,
        "currency": "USD",
        "area_hectares": 50.0,
        "property_type": "farmland",
        "location": {
            "address": "Km 15 Route de Meknès",
            "city": "Fès",
            "state": "Fès-Meknès",
            "country": "Morocco",
        },
        "features": ["Irrigation", "Fertile soil"],
        "water_access": True,
        "road_access": True,
    }
    resp = await auth_client.post("/api/v1/properties/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "50 Hectare Organic Farm"
    assert data["price"] == 250000.0
    assert data["status"] == "available"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_properties(auth_client: AsyncClient):
    await auth_client.post("/api/v1/properties/", json={
        "title": "Farm 1",
        "description": "Desc 1",
        "price": 100000,
        "currency": "USD",
        "area_hectares": 20,
        "property_type": "farmland",
        "location": {"address": "A", "city": "City", "state": "State", "country": "Country"},
    })
    await auth_client.post("/api/v1/properties/", json={
        "title": "Farm 2",
        "description": "Desc 2",
        "price": 200000,
        "currency": "USD",
        "area_hectares": 30,
        "property_type": "ranch",
        "location": {"address": "B", "city": "City2", "state": "State2", "country": "Country"},
    })
    resp = await auth_client.get("/api/v1/properties/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_get_property_by_id(auth_client: AsyncClient):
    create_resp = await auth_client.post("/api/v1/properties/", json={
        "title": "Specific Farm",
        "description": "Test",
        "price": 150000,
        "currency": "USD",
        "area_hectares": 25,
        "property_type": "farmland",
        "location": {"address": "X", "city": "Y", "state": "Z", "country": "W"},
    })
    prop_id = create_resp.json()["id"]

    resp = await auth_client.get(f"/api/v1/properties/{prop_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Specific Farm"


@pytest.mark.asyncio
async def test_update_property(auth_client: AsyncClient):
    create_resp = await auth_client.post("/api/v1/properties/", json={
        "title": "Original",
        "description": "Original desc",
        "price": 100000,
        "currency": "USD",
        "area_hectares": 10,
        "property_type": "farmland",
        "location": {"address": "A", "city": "B", "state": "C", "country": "D"},
    })
    prop_id = create_resp.json()["id"]

    resp = await auth_client.put(f"/api/v1/properties/{prop_id}", json={"title": "Updated Title", "price": 200000})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"
    assert resp.json()["price"] == 200000.0


@pytest.mark.asyncio
async def test_delete_property(auth_client: AsyncClient):
    create_resp = await auth_client.post("/api/v1/properties/", json={
        "title": "To Delete",
        "description": "Will be deleted",
        "price": 50000,
        "currency": "USD",
        "area_hectares": 5,
        "property_type": "farmland",
        "location": {"address": "A", "city": "B", "state": "C", "country": "D"},
    })
    prop_id = create_resp.json()["id"]

    resp = await auth_client.delete(f"/api/v1/properties/{prop_id}")
    assert resp.status_code == 204

    get_resp = await auth_client.get(f"/api/v1/properties/{prop_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_properties_by_type(auth_client: AsyncClient):
    await auth_client.post("/api/v1/properties/", json={
        "title": "Farmland",
        "description": "A farm",
        "price": 100000,
        "currency": "USD",
        "area_hectares": 20,
        "property_type": "farmland",
        "location": {"address": "A", "city": "B", "state": "C", "country": "D"},
    })
    await auth_client.post("/api/v1/properties/", json={
        "title": "Ranch",
        "description": "A ranch",
        "price": 200000,
        "currency": "USD",
        "area_hectares": 50,
        "property_type": "ranch",
        "location": {"address": "E", "city": "F", "state": "G", "country": "H"},
    })
    resp = await auth_client.get("/api/v1/properties/?property_type=ranch")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    assert resp.json()["items"][0]["property_type"] == "ranch"
