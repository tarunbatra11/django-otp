"""
List of endpoints available.
"""

from collections import OrderedDict

from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from api.serializers import (
    CreateUserSerializer,
)
from api import helpers
from otp.models import Mapping
from otp.extended import oauth2_validators


class CreateUserAPI(APIView):
    """
    Create user instance. For this API permission are not needed.
    """
    serializer_class = CreateUserSerializer

    def put(self, request, format=None):

        # check if phone is given in request
        if 'phone' not in request.data['account']:
            raise ValueError('Phone field is required')

        # check for secret_identifier
        phone_in_request = request.data['account']['phone']
        secret_identifier = request.data['secret_identifier']
        # TODO: take get_object from common library
        verification_instance = oauth2_validators.get_object('verification',
                                                             'phone',
                                                             phone_in_request)
        if verification_instance.secret_identifier != secret_identifier:
            raise Exception('Secret identifier does not match')

        # check for user in Mapping table
        mapping_instance = None
        try:
            mapping_instance = Mapping.objects.get(
                phone=request.data['account']['phone'])
        except Mapping.DoesNotExist:
            pass

        if mapping_instance:
            raise ValueError('User with this number is already registered')

        # extra checks if auto_username is selected
        if 'auto_username' in request.data \
           and 'username' not in request.data \
           and request.data['auto_username']:
            request.data['username'] = helpers.generate_username()
            request.data['password'] = helpers.generate_password()

            # check for number verification and expiry from temporary
            # table(Verification)
            if not verification_instance.verified:
                raise ValueError('Number not verified')
            expiry = verification_instance.expiry + timezone.timedelta(
                seconds=60)
            if timezone.now() > expiry:
                raise ValueError('Expiry over')
            verification_instance.alias = request.data['username']
            verification_instance.save()
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # making entry in permanent table(Mapping)
            user_phone_mapping = Mapping(
                phone=request.data['account']['phone'],
                alias=request.data['username'])
            user_phone_mapping.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class CreateEnquiryAPI(APIView):
#    """
#    Create request instance.
#    """
#    serializer_class = CreateEnquirySerializer
#
#    def put(self, request, format=None):
#        serializer = CreateEnquirySerializer(data=request.data,
#                                             context={'request': request})
#        if serializer.is_valid():
#            serializer.save(user=request.user)
#            actions.mark_requested_and_increase_num_requested(request.user)
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class UserAPI(APIView):
#    """
#    User object endpoint, for particular user.
#    """
#    permission_classes = [permissions.IsAuthenticated, IsOwner]
#    serializer_class = UserSerializer
#
#    def get_object(self, request, pk):
#        try:
#            obj = User.objects.get(pk=pk)
#            self.check_object_permissions(request, obj)
#            return obj
#        except User.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        user = self.get_object(request, pk)
#        serializer = UserSerializer(user)
#        return Response(serializer.data)
#
#    # TODO: consider not to update phone number
#    def post(self, request, pk, format=None):
#        user = self.get_object(request, pk)
#        stored_user_data = UserSerializer(user)
#        stored_user_data = stored_user_data.data
#        updated_user_data = stored_user_data.copy()
#        updated_account_data = updated_user_data['account']
#        updated_account_data = dict(updated_account_data)
#        account_fields = ['blood_group', 'dob', 'phone', 'address',
#                          'zip_code', 'verified']
#        not_allowed_to_change = ['phone', 'verified']
#        for key, value in request.data.items():
#            if key in account_fields and key not in not_allowed_to_change:
#                updated_account_data[key] = value
#            else:
#                updated_user_data[key] = value
#        updated_account_data = OrderedDict(updated_account_data)
#        updated_user_data['account'] = updated_account_data
#        serializer = UserSerializer(user, data=updated_user_data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        user = self.get_object(request, pk)
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


#class EnquiryAPI(APIView):
#    """
#    Enquiry object endpoint, for particular user.
#    """
#    permission_classes = [permissions.IsAuthenticated, IsOwner]
#    serializer_class = EnquirySerializer
#
#    def get_object(self, request, pk):
#        try:
#            obj = User.objects.get(pk=pk)
#            self.check_object_permissions(request, obj)
#            return obj
#        except User.DoesNotExist:
#            raise Http404
#
#    def get_enquiry_object(self, request, pk):
#        try:
#            enquiry = Enquiry.objects.get(pk=pk)
#            enquiry_owner = User.objects.get(pk=enquiry.user_id)
#            enquiry_owner_id = enquiry_owner.id
#            if self.get_object(request, enquiry_owner_id):
#                return enquiry
#            else:
#                return Response('Access denied.')
#        except Enquiry.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        enquiry = self.get_enquiry_object(request, pk)
#        serializer = EnquirySerializer(enquiry)
#        return Response(serializer.data)
#
#    def post(self, request, pk, format=None):
#        enquiry = self.get_enquiry_object(request, pk)
#        serializer = EnquirySerializer(enquiry, data=request.data,
#                                       partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        else:
#            return Response('access denied')
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        enquiry = self.get_enquiry_object(request, pk)
#        enquiry.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


#class ListUserAPI(APIView):
#    """
#    Provides user list based on query.
#    """
#    permission_classes = [permissions.IsAuthenticated]
#
#    def get(self, request, format=None):
#        params = {}
#        integer_list = ['id']
#        for key, value in request.query_params.items():
#            if key in integer_list:
#                params[key] = int(value)
#            else:
#                params[key] = value
#        user = User.objects.filter(**params)
#        serializer = ListUserSerializer(user, many=True)
#        return Response(serializer.data)


#class ListEnquiryAPI(APIView):
#    """
#    Provides request list based on query.
#    """
#    permission_classes = [permissions.IsAuthenticated]
#
#    def get(self, request, format=None):
#        params = {}
#        integer_list = ['id']
#        for key, value in request.query_params.items():
#            if key in integer_list:
#                params[key] = int(value)
#            else:
#                params[key] = value
#        requests = Enquiry.objects.filter(**params)
#        serializer = ListEnquirySerializer(requests, many=True)
#        return Response(serializer.data)
