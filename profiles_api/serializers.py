from rest_framework import serializers
#access te UserProfile model
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    # in the browser a 'name' input field will appear
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    # we use a metaclass to configure the serializer to point to a specific model
    class Meta:
        model = models.UserProfile
        # we define the fields we want to manage with the serializer
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                # this is just for the browsable API
                'style': {'inut_type': 'password'}
            }
        }

    # we override the create function because we wan to store the password
    # as a hash (the default is plain text)
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user
