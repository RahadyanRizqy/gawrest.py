from fastapi import APIRouter
from fastapi import Depends
from middleware.auth import JWTBearer
import handlers

router = APIRouter()

router.add_api_route(
    "/", 
    handlers.root, 
    methods=["GET"]
)

router.add_api_route(
    "/gems",
    handlers.gems,
    methods=["GET", "POST"],
    dependencies=[Depends(JWTBearer())]
)

router.add_api_route(
    "/gems/{gem_id}",
    handlers.gems,
    methods=["GET", "PUT", "DELETE"],
    dependencies=[Depends(JWTBearer())]
)

router.add_api_route(
    "/chat",
    handlers.chat,
    methods=["POST"],
    dependencies=[Depends(JWTBearer())]
)

router.add_api_route(
    "/chat/{gem_id}", 
    handlers.chat, 
    methods=["POST"],
    dependencies=[Depends(JWTBearer())]
)