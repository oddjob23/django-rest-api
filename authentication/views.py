from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (RegisterSerializer, LoginSerializer)
from .renderers import UserJSONRenderer
# Create your views here.


class RegistrationAPIView(APIView):
    # AllowAny - anybody can access this view point
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegisterSerializer

    def post(self, request):
        # instance of request.user
        user = request.data.get('user', {})
        # create, validate and save serializer
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return response - ALWAYS return response
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # create serializer
        serializer = self.serializer_class(data=user)
        # validate serializer
        serializer.is_valid(raise_exception=True)
        # no need to save serializer - this method should only verify the user input

        # return Response
        return Response(serializer.data, status=status.HTTP_200_OK)
