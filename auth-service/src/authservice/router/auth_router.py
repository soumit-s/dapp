from fastapi import APIRouter, HTTPException, status
from typing import Annotated

from ..models import VerifyPhoneOtpDTO, SendPhoneOtpDTO
from ..services import JWTService, UserService
from ..deps import GetJwtServiceDep, GetUserServiceDep

router = APIRouter()


@router.post("/cust/send-otp/phone")
async def send_otp_to_phone(body: SendPhoneOtpDTO):
    """
    Used by customers to register/login using there phone numbers.
    Returns a verification flow id.
    """
    pass


@router.post("/cust/verify-otp")
async def verify_otp(
    body: VerifyPhoneOtpDTO,
    jwt_service: Annotated[JWTService, GetJwtServiceDep],
    user_service: Annotated[UserService, GetUserServiceDep],
) -> str:
    if body.otp != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP does not match"
        )
    user = await user_service.upsert_user(body.phone)
    jwt = jwt_service.generate_user_token(user.id)
    return jwt
