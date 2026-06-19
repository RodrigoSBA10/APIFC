import httpx

BASE_URL = "https://www.thesportsdb.com/api/v1/json/123"


async def buscar_equipo_web(nombre: str):
    url = f"{BASE_URL}/searchteams.php"
    params = {"t": nombre}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def buscar_jugador_web(nombre: str):
    url = f"{BASE_URL}/searchplayers.php"
    params = {"p": nombre}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()