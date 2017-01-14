from datetime import timedelta
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import (
    AccessToken,
    RefreshToken,
    AbstractApplication
)
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils import timezone

from api.models import Account
from otp.models import Verification, Mapping


GRANT_TYPE_MAPPING = {
    'authorization_code': (AbstractApplication.GRANT_AUTHORIZATION_CODE,),
    'password': (AbstractApplication.GRANT_PASSWORD,),
    'client_credentials': (AbstractApplication.GRANT_CLIENT_CREDENTIALS,),
    'refresh_token': (AbstractApplication.GRANT_AUTHORIZATION_CODE,
                      AbstractApplication.GRANT_PASSWORD,
                      AbstractApplication.GRANT_CLIENT_CREDENTIALS),
    'otp': ('otp',)
}


class ExtendedOAuth2Validator(OAuth2Validator):

    def validate_user(self, phone, client, request, *args, **kwargs):
        """
        Check username and password correspond to a valid and active User
        """
        data_dict = get_request_body_dict(request)

        request_phone = data_dict['phone']

        # check phone length
        if len(str(request_phone)) != 10:
            raise ValueError('Phone number should have 10 digits')

        if data_dict['grant_type'] == 'otp':
            mapped_object = get_object('mapping', 'phone', request_phone)
            # check if access already granted then use refresh token
            if mapped_object.access_token_granted:
                raise Exception('Access token provided, use refresh token')
            else:
                # check if verification is done and expiry is not over
                verification_object = get_object('verification', 'phone',
                                                 request_phone)
                expiry_time = verification_object.expiry
                added_expiry_time = timezone.timedelta(seconds=300)
                expiry = expiry_time + added_expiry_time
                if timezone.now() > expiry:
                    raise Exception('Code has expired')

                if verification_object and not verification_object.verified:
                    raise Exception('Number is not verified')

                # check for username and password in mapping and user table
                account_object = get_object('account', 'phone', request_phone)
                user_object = get_object('user', 'id', account_object.user_id)
                user_object = User.objects.get(id=account_object.user_id)
                if mapped_object.alias != user_object.username or mapped_object.phone != account_object.phone:
                    raise Exception('Username and phone mismatch')
                # check if user is active or not
                if not user_object.is_active:
                    raise Exception('User not active')
                mapped_object.access_token_granted = True
                mapped_object.save()
                return True
        else:
            raise Exception('Grant type otp is for first time access for otp')
        return False

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        """
        Validate both grant_type is a valid string and grant_type is allowed
        for current workflow
        """
        assert(grant_type in GRANT_TYPE_MAPPING)  # mapping misconfiguration
        return request.client.authorization_grant_type in GRANT_TYPE_MAPPING[grant_type]

    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        Save access and refresh token, If refresh token is issued, remove old
        refresh tokens as in rfc:`6`
        """
        if request.refresh_token:
            # remove used refresh token
            try:
                RefreshToken.objects.get(token=request.refresh_token).revoke()
            except RefreshToken.DoesNotExist:
                assert()  # TODO though being here would be very strange, at least log the error

        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        if request.grant_type == 'client_credentials':
            request.user = None

        # TODO: get user from phone number in request, there should be some
        # secure system to get user from phone number
        data_dict = get_request_body_dict(request)
        phone = str(data_dict['phone'])
        account_object = get_object('account', 'phone', phone)
        user_object = get_object('user', 'id', account_object.user_id)

        access_token = AccessToken(
            user=user_object,
            scope=token['scope'],
            expires=expires,
            token=token['access_token'],
            application=request.client)
        access_token.save()

        if 'refresh_token' in token:
            refresh_token = RefreshToken(
                user=user_object,
                token=token['refresh_token'],
                application=request.client,
                access_token=access_token
            )
            refresh_token.save()

        # TODO check out a more reliable way to communicate expire time to oauthlib
        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS


def get_request_body_dict(request):
    request_body = request.body
    request_data = request_body.split('&')
    data_dict = {}
    for data in request_data:
        parts = data.split('=')
        data_dict[parts[0]] = parts[1]
    return data_dict


def get_object(model, column, value):
    maps = {'user': User, 'account': Account,
            'verification': Verification, 'mapping': Mapping}
    if column == 'phone':
        fetched_object = get_object_from_phone(model, value, maps)
    elif column == 'id':
        fetched_object = get_object_from_id(model, value, maps)
    return fetched_object


def get_object_from_phone(model, value, maps):
    try:
        fetched_object = maps[model].objects.get(phone=value)
    except ObjectDoesNotExist:
        raise Exception('Object does not exist')
    except MultipleObjectsReturned:
        raise Exception('Multiple objects returned')
    except Exception:
        raise Exception('Object could not be returned')
    return fetched_object


def get_object_from_id(model, value, maps):
    try:
        fetched_object = maps[model].objects.get(id=value)
    except ObjectDoesNotExist:
        raise Exception('Object does not exist')
    except MultipleObjectsReturned:
        raise Exception('Multiple objects returned')
    except Exception:
        raise Exception('Object could not be returned')
    return fetched_object
