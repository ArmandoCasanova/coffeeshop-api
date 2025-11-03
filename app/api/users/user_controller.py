from app.core.http_response import CoffeeAppHttpResponse
from uuid import UUID
from fastapi import HTTPException
from app.api.users.user_service import UserService
from app.api.users.user_schema import UserResponseSchema, UserUpdateSchema


class UserController:
    def __init__(self, session):
        self.user_service = UserService(session)

    async def get_user_profile(self, user_id: UUID) -> UserResponseSchema:
        try:
            user = await self.user_service.get_user_profile(user_id)
            return UserResponseSchema.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_profile(
        self, user_id: UUID, user_data: UserUpdateSchema
    ) -> UserResponseSchema:
        try:
            updated_user = await self.user_service.update_user_profile(
                user_id, user_data
            )
            return UserResponseSchema.model_validate(updated_user)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    # async def get_user_points(self, user_id: UUID) -> UserPointsResponseSchema:
    #     try:
    #         user = await self.user_service.get_user_profile(user_id)
    #         return UserPointsResponseSchema(user_id=user.user_id, points=user.points)
    #     except HTTPException:
    #         raise
    #     except Exception as e:
    #         CoffeeAppHttpResponse.internal_error()

    async def change_user_password(
        self, user_id: UUID, old_password: str, new_password: str
    ) -> dict:
        try:
            result = await self.user_service.change_user_password(
                user_id, old_password, new_password
            )
            return result
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
