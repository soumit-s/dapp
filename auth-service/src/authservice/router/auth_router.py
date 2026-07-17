from fastapi import APIRouter, HTTPException, status
from fastapi import Header, Response
from typing import Annotated

from ..models import VerifyPhoneOtpDTO, SendPhoneOtpDTO, AdminBasicLoginDTO
from ..services import JWTService, UserService, AuthService
from ..deps import (
    GetJwtServiceDep,
    GetUserServiceDep,
    GetAuthServiceDep,
    GetBearerTokenDep,
)
from ..errors import InvalidTokenError, UserNotFoundError, UserNotAuthorizedError

router = APIRouter()


@router.post("/admin/auth/login/basic")
async def admin_login(
    body: AdminBasicLoginDTO, auth_service: Annotated[AuthService, GetAuthServiceDep]
) -> str:
    try:
        token = await auth_service.admin_login(body.email, body.password)
        return token
    except (UserNotAuthorizedError, UserNotFoundError) as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/auth/cust/send-otp/phone")
async def send_otp_to_phone(body: SendPhoneOtpDTO):
    """
    Used by customers to register/login using there phone numbers.
    Returns a verification flow id.
    """
    pass


@router.post("/auth/cust/verify-otp")
async def verify_otp(
    body: VerifyPhoneOtpDTO, auth_service: Annotated[AuthService, GetAuthServiceDep]
) -> str:
    try:
        return await auth_service.user_verify_otp(body.phone, body.otp)
    except UserNotAuthorizedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP does not match"
        )


@router.get("/auth/validate")
async def validate_jwt(
    jwt_service: Annotated[JWTService, GetJwtServiceDep],
    token: Annotated[str, GetBearerTokenDep],
):
    """
    Validated bearer token. Populates X-User-Id, X-User-Role headers in the response.
    X-User-Id: Contains the user id as a string
    X-User-Role: List of roles separated by a comma(,)
    """
    try:
        payload = jwt_service.validate(token)
        headers = {"X-User-Id": str(payload.id), "X-User-Role": ",".join(payload.role)}
        return Response(headers=headers, status_code=status.HTTP_200_OK)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.__str__()
        )
    