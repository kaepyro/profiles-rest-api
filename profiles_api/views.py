from rest_framework.views import APIView
from rest_framework.response import Response


# it works by defining an url as an endpoint and assigning to the View
# it expects a different functions for each http requests
class HelloApiView(APIView):
    """Test API View"""

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
