"""@Kaizuryu"""

from io import BytesIO
from ErinaBot import aiohttpsession

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "ErinaBot_Carbon.png"
    return image
