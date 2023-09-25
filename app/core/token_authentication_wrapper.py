from auditlog.middleware import AuditlogMiddleware
from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationWrapper(TokenAuthentication):
    def authenticate(self, request):
        user, token = super().authenticate(request)
        request.user = user # necessary for preventing recursion
        AuditlogMiddleware().process_request(request)
        return user, token