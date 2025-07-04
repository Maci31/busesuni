from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError
from auth.config import keycloak_openid
from auth.models import UserInfo

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> str:
        try:
            token = keycloak_openid.token(username, password)
            return token["access_token"]
        except KeycloakAuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrecta"
            )

    @staticmethod
    def verify_token(token: str):
        try:
            user_info = keycloak_openid.userinfo(token)
            print(user_info)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalido"
                )
            return UserInfo(
                preferred_username=user_info["preferred_username"],
                email=user_info.get("email"),
                full_name=user_info.get("name"),
            )
        except KeycloakAuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se puede validar las credenciales"
            )








