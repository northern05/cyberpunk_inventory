from fastapi import FastAPI, APIRouter

from .items.views import router as items_router
from .auth.views import router_token

router = APIRouter()
router.include_router(router=items_router, prefix="/items")
router.include_router(router=router_token, prefix="/auth")

api = FastAPI(title='NFT API', version='0.0.1')

