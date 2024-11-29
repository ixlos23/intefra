from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Film
from apps.serializers import RegisterUserModelSerializer, LoginUserModelSerializer, FilmSerializer


@extend_schema(tags=['Login_Register'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserModelSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Successfully registered!'
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Login_Register'])
class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    # This method should be defined for GenericAPIView to work correctly
    def get_serializer_class(self):
        return LoginUserModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # This will work now
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


"""


[Unit]
Description=Django Service
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/ixlos_/intefra
ExecStart=/var/www/ixlos_/intefra/.venv/bin/python3 /var/www/ixlos_/intefra.venv/bin/gunicorn --workers 1 --bind unix:/var/www/ixlos_/intefra/django.sock root.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
  
  

server {
    listen 8084;
    server_name 157.245.192.13;

    location /static/ {
        root /var/www/ixlos_/intefra;
    }

    location /media/ {
        root /var/www/ixlos_/intefra;
    }

     location / {
         include         proxy_params;
         proxy_pass http://unix:/var/www/ixlos_/intefra/project.sock;
     }

    error_log  /var/log/nginx/project-back-error.log;
    access_log /var/log/nginx/project-back-access.log;
}


"""


@extend_schema(tags=['Film'])
class FilmCreateAPIView(CreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer



@extend_schema(tags=['Film'])
class FilmListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
