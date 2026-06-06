from fastapi import APIRouter,Cookie,HTTPException,Depends
from app.services.user_service import login,register
from app.schemas.user import LoginRequest,RegisterRequest
from fastapi import Response
from app.utils.jwt_util import create_access_token,verify_token
from app.db.database import get_connection
router = APIRouter(tags=["Auth"],prefix='/auth')

@router.post('/login')
def login_handler(user:LoginRequest,response:Response,conn = Depends(get_connection)):
    result = login(user,conn)

    token = create_access_token({
        "email": user.email
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="none",
    )

    return result


@router.post('/register')
def register_handler(user:RegisterRequest,response : Response,conn = Depends(get_connection)):
    result = register(user,conn)

    token = create_access_token({
        "email": user.email
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="none",
    )

    return result

@router.get('/user')
def get_user(access_token: str = Cookie(None)):
    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return {
        "email": payload["email"]
    }
