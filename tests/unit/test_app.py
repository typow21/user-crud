import pytest

class TestApp:

    @pytest.mark.asyncio
    async def test_app_start(self, client):
        url = "http://localhost:8000/" 
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == {"Hello": "World"}