from rest_framework.views import APIView
from rest_framework.response import Response
# status object: http status codes
from rest_framework import status
# this is the serializer what we created
from profiles_api import serializers
# basic class fro viewsets
from rest_framework import viewsets
# for filtering i.e. search user by name
from rest_framework import filters
# for login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings



from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions

from profiles_api import models


# it works by defining an url as an endpoint and assigning to the View
# it expects a different functions for each http requests
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    # request is passed by django rest_framework format is adding and ending suffix
    # to the endpoint url. Best practice to keep there, just in case.
    # the element of the list are for demonstrartion purposes, how to
    # return an object by an APIView
    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
        'Uses HTTP methods as function (get, post, patch, put, delete)',
        'Is similar to a traditional Django View',
        'Gives you the most control over your application logic',
        'Is mapped manually to URLs'
        ]

        # The Response object will be converted to Json. In order to be converted to json
        # the returned object has to be a list or a dictionary
        return Response({'message': 'Hello','an_apiview': an_apiview})

    # Handling http post request
    def post(self, request):
        """Create a hello message with our name"""
        # retrieve the serializer and pass the data recieved from the request
        # self.serializer_class function comes with the APIView
        # standard way retrieve the serializer class
        serializer = self.serializer_class(data=request.data)

        # the serializer class can also validate the input
        # so here, its max length can be 10 character
        if serializer.is_valid():
            # you can retrieve any field this way that you defined in the
            # serializer
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        # if the input is not valid:
        else:
            return Response(
                #return the errors generated by the serializer based on our rules
                serializer.errors,
                #also return the error code
                status=status.HTTP_400_BAD_REQUEST
                )

    # handling http put request
    # pk: ID of the object what you update
    # in the examples above we won't update any object!
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    # patch only updates a field which is provided in the request
    # if you have a first name and a last name field and only provide
    # a first name, it will update it and does not change the last name
    # the same with the put would remove the last name!
    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delet an object"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    #we can use the same serializer like in the views above
    serializer_class = serializers.HelloSerializer

    # list a set of objects what the viewset represents
    def list(self, request):
        """Return a hello message"""

        a_viewset =[
        'Uses actions (list, create, retrieve, update, partial_update',
        'Automatically maps to URLs using Routers',
        'Provides more functionality with less code',
        ]

        return Response({"message": 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
            serializer.error,
            status=status.HTTP_400_BAD_REQUEST
            )

    #pk: primary key
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})

#django knows the standard functions on a ModelViewSet(create, list, update,
#partial_update, destroy)
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    # adding all of the authentication classes to the class variable
    # it generates a random token when the user logges in and we add this
    # token to every request a user made
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    # add filtering options
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    # we have to override this class to see in the browsable api
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
