from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from api.models import Account


###################################################
#               user serializers                  #
###################################################


class AccountSerializer(ModelSerializer):
    """
    Provide serialized account information.
    """
    class Meta:
        model = Account
        fields = ('phone',)


class CreateUserSerializer(ModelSerializer):
    """
    Creates new user instance and save in database.
    """
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name',
                  'last_name', 'account',)

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        # TODO: make sure either all 3 tables get data or none
        # if this is true user_id should always be equal to
        # corresponding record's id
        user.save()
        Account.objects.create(user=user, **account_data)
        return user
