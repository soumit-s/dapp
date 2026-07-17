from fastapi import Depends, Header, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from .db import DB
from .config import load_config
from .services import StoreService
from .models import UserRole, UserDetailsDTO

config_singleton = load_config()
db_singleton = DB(url=config_singleton.database_url)


GetConfigDep = Depends(lambda: config_singleton)
GetDbDep = Depends(lambda: db_singleton)


async def get_db() -> DB:
    return db_singleton


async def get_db_async_engine(db: Annotated[DB, GetDbDep]) -> AsyncEngine:
    return db.get_async_engine()


GetDbAsyncEngineDep = Depends(get_db_async_engine)


async def get_db_async_session_factory(
    db: Annotated[DB, GetDbDep],
) -> async_sessionmaker[AsyncSession]:
    return db.get_async_session_factory()


GetDbAsyncSessionFactoryDep = Depends(get_db_async_session_factory)


async def get_db_async_session(
    factory: Annotated[async_sessionmaker[AsyncSession], GetDbAsyncSessionFactoryDep],
):
    async with factory() as session:
        yield session


GetDbAsyncSessionDep = Depends(get_db_async_session)


async def get_store_service(session: Annotated[AsyncSession, GetDbAsyncSessionDep]):
    return StoreService(session)


GetStoreServiceDep = Depends(get_store_service)


async def get_user_details(
    x_user_id: Annotated[str | None, Header()],
    x_user_role: Annotated[str | None, Header()],
) -> UserDetailsDTO:
    if x_user_id == None or x_user_role == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    roles = x_user_role.split(",")

    try:
        details = UserDetailsDTO(user_id=int(x_user_id), roles=set())
        if details.user_id < 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        for str_role in roles:
            details.roles.add(UserRole(str_role))

        return details
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# Extracts user details from the Request(X-User-Id, X-User-Role).
GetUserDetailsDep = Depends(get_user_details)

async def get_admin(user_details: Annotated[UserDetailsDTO, GetUserDetailsDep]) -> UserDetailsDTO:
    if UserRole.ADMIN not in user_details.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user_details

# Requires the user must be an admin. Also returns the extracted UserDetailsDTO. Check
# out GetUserDetailsDep for more information.
GetAdminDep = Depends(get_admin)