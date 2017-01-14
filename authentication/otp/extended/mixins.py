from oauth2_provider.views import TokenView

from otp.extended.oauth2_backends import ExtendedOAuthLibCore
from otp.extended.pre_configured import ExtendedServer


class ExtendedTokenView(TokenView):

    def create_token_response(self, request):
        """
        Use ExtendedOAuthLibcore and ExtendedServer instead of OAuthLibCore
        and Server
        """
        core = ExtendedOAuthLibCore(ExtendedServer)
        return core.create_token_response(request)
