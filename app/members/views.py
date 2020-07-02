from django.contrib.auth import get_user_model, authenticate

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from members.models import FollowRelations
from members.serializers import UserSerializer, FollowRelationsSerializer

User = get_user_model()


class UserModelViewAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('아이디 또는 비밀번호가 올바르지 않습니다.')
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            data = {
                'message': 'token create',
                'user': UserSerializer(request.user).data,
                'token': token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'message': 'token get',
            'user': UserSerializer(request.user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        user = request.user
        if user.auth_token:
            user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowModelViewAPI(viewsets.ModelViewSet):
    queryset = FollowRelations.objects.all()
    serializer_class = FollowRelationsSerializer

    # @action(detail=True, methods=['post'])
    # def is_following(self, request, pk=None):
    #     user = FollowRelations.objects.save(to_relation=pk)
    #     return Response(user, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        if request.user.pk == int(request.data['to_relation']):
            return Response('You can not follow or block yourself', status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            saved_data = FollowRelations.objects.get(from_relation=self.request.user.pk,
                                                     to_relation=self.request.data['to_relation'])
            saved_data.relation_type = self.request.data['relation_type']
            saved_data.save()
        except:
            serializer.save()
