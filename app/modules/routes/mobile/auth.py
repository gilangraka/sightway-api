from fastapi import APIRouter, Depends
from app.modules.schemas import TokenSchema
from app.modules.controllers.auth import login, register

router = APIRouter(prefix="/auth", tags=["Auth Mobile (Pemantau/Penyandang)"])

@router.post("/login/pemantau", response_model=TokenSchema)
async def login_pemantau_handler(token: TokenSchema = Depends(login({"pemantau"}))):
    return token

@router.post("/login/penyandang", response_model=TokenSchema)
async def login_penyandang_handler(token: TokenSchema = Depends(login({"penyandang"}))):
    return token

@router.post("/register/pemantau", response_model=TokenSchema)
async def register_pemantau_handler(token: TokenSchema = Depends(register("pemantau"))):
    return token

@router.post("/register/penyandang", response_model=TokenSchema)
async def register_penyandang_handler(token: TokenSchema = Depends(register("penyandang"))):
    return token