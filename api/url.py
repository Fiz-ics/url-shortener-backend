from data import mongo
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    uri = await mongo.get_uri()
    router.client = AsyncIOMotorClient(uri)
    router.db = router.client.url


@router.on_event("shutdown")
def shutdown_event():
    router.client.close()


@router.get('/{url_id}')
async def get_url(url_id: str):
    collection = router.db.links
    result = await mongo.get_url(collection, url_id)
    return RedirectResponse(result["url"])
