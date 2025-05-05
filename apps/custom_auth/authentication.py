from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication to provide more detailed error messages.
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Token inválido o expirado')

        if not token.user.is_active:
            raise AuthenticationFailed('Usuario inactivo o eliminado')

        return (token.user, token)