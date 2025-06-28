from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:7080",
    realm_name="busesuni",
    client_id="busesuni",
    client_secret_key="b1gNBZIdLHrtIga2KUNO65IKlzl585pS"
)

# Configuración de KeycloakAdmin
keycloak_admin = KeycloakAdmin(
    server_url="http://localhost:7080",
    username="20214517i",  # Usuario administrador
    password="1234",  # Contraseña del administrador
    realm_name="busesuni",  # Nombre del realm
    verify=True
)


def get_openid_config():
    return keycloak_openid

def get_admin_config():
    return keycloak_admin