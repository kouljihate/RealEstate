import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient, clean_db):
    payload = {
        "email": "farmer@test.com",
        "username": "farmer1",
        "password": "TestPass123",
        "full_name": "Test Farmer",
        "phone": "+212600000000",
    }
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "farmer@test.com"
    assert data["role"] == "customer"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient, clean_db):
    payload = {
        "email": "dup@test.com",
        "username": "dupuser",
        "password": "TestPass123",
        "full_name": "Dup User",
    }
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient, clean_db):
    await client.post("/api/v1/auth/register", json={
        "email": "login@test.com",
        "username": "loginuser",
        "password": "TestPass123",
        "full_name": "Login User",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@test.com",
        "password": "TestPass123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, clean_db):
    await client.post("/api/v1/auth/register", json={
        "email": "wrong@test.com",
        "username": "wronguser",
        "password": "TestPass123",
        "full_name": "Wrong User",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wrong@test.com",
        "password": "BadPass",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, clean_db):
    await client.post("/api/v1/auth/register", json={
        "email": "me@test.com",
        "username": "meuser",
        "password": "TestPass123",
        "full_name": "Me User",
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "me@test.com",
        "password": "TestPass123",
    })
    token = login_resp.json()["access_token"]

    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@test.com"
