from uuid import UUID, uuid4

from schemas.user import UserCreate, UserDB, UserResponse

fake_db: dict[UUID, UserDB] = dict()


class AuthService:
    async def register(
        self,
        user: UserCreate,
    ) -> UserResponse:
        hashed_password = user.password  # TODO: Hash
        # TODO: Verify user exists
        # TODO: Real DB
        user_data = {
            "user_id": uuid4(),
            "username": user.username,
            "hashed_password": hashed_password,
        }
        user_db = UserDB(**user_data)
        fake_db[user_data["user_id"]] = user_db
        print(fake_db)
        user_response_data = {
            "username": user_db.username,
            "user_id": user_db.user_id,
        }
        user_response = UserResponse(**user_response_data)
        return user_response


def get_auth_service():
    return AuthService()
