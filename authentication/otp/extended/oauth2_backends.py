from oauth2_provider.oauth2_backends import OAuthLibCore
#from oauth2_provider.settings import oauth2_settings

from otp.extended.pre_configured import ExtendedServer
from otp.extended.oauth2_validators import ExtendedOAuth2Validator


class ExtendedOAuthLibCore(OAuthLibCore):

    def __init__(self, server=None):
        """
        Use ExtendedServer instead of Server
        """
        #self.server = ExtendedServer(oauth2_settings.OAUTH2_VALIDATOR_CLASS())
        self.server = ExtendedServer(ExtendedOAuth2Validator())
