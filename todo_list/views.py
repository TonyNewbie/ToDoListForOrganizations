from .authentication import EmailBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.cache import cache
from .models import Task, Organization
from .serializers import UserSerializer, TaskSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# Disable csrf check
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


def get_request_params(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    organization = request.data.get('organization', '')
    return email, password, organization


class UserAuthenticationView(APIView):
    def post(self, request):
        email, password, organization = get_request_params(request)
        # use custom authentication scheme
        authentication = EmailBackend()
        user = authentication.authenticate(request, username=email, password=password, organization=organization)
        if user is None:
            return Response({'error': 'User does not exist in organization'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        # assign the organization to the user session
        request.session['organization'] = organization
        cache.set(request.session.session_key, user.email, 60*60*24)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request):
        if not request.session.session_key:
            return Response({'errors': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        cache.delete(request.session.session_key)
        logout(request)
        return Response(status=status.HTTP_200_OK)


# GET task list, POST new task
class TaskListView(ListCreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        organization = self.request.session['organization']
        owner = Organization.objects.get(name=organization)
        return serializer.save(owner=owner)

    def get_queryset(self):
        organization = self.request.session['organization']
        return Task.objects.filter(owner__name=organization)


# GET, PATCH, PUT one task
class SingleTaskView(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        organization = self.request.session['organization']
        return Task.objects.filter(owner__name=organization)
