from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, AuthTokenSerialier, UserAvatarSerializer

from core.models import User


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Get users list"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get_permissions(request):
    #     logged_in_user = request.user
    #     return Response(data=logged_in_user.get_all_permissions())

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.all().order_by('-name')
    
    def get_serializer_class(self):
        """return apropriate serializer class"""
        if self.action == 'retrieve':
            return UserSerializer
        elif self.action == 'upload_image':
            return UserAvatarSerializer
        
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload avatar to User"""
        user = self.get_object()
        serialzier = self.get_serializer(
            user,
            data=request.data
        )

        if serialzier.is_valid():
            serialzier.save()
            return Response(
                serialzier.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serialzier.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer = AuthTokenSerialier
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
