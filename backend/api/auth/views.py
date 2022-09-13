from django.conf import settings
from django.contrib.auth import login as _login
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from api.auth.serializers import LoginRequestSerializer, SendVerificationLinkRequestSerializer, \
    ResetPasswordRequestSerializer, TokenResponse, UserIdResponse
from api.helpers import parse_request_data
from bis.emails import email_text
from bis.models import User
from login_code.models import LoginCode


def login_and_return_token(request, user):
    _login(request._request, user)
    return Response({'token': user.auth_token.key})


@extend_schema(responses=UserIdResponse())
@api_view()
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({'id': request.user.id})


@extend_schema(request=LoginRequestSerializer,
               responses={
                   200: TokenResponse,
                   401: OpenApiResponse(description='E-mail or password incorrect'),
                   429: OpenApiResponse(description='Too many requests'),
               })
@api_view(['post'])
@parse_request_data(LoginRequestSerializer)
def login(request, data):
    user = User.objects.filter(all_emails__email=data['email']).first()
    if not user:
        raise AuthenticationFailed()

    LoginCode.check_throttled(user)

    if not user.check_password(data['password']):
        raise AuthenticationFailed()

    return login_and_return_token(request, user)


@extend_schema(request=SendVerificationLinkRequestSerializer,
               responses={
                   HTTP_204_NO_CONTENT: None,
                   404: OpenApiResponse(description='User with email not found'),
                   429: OpenApiResponse(description='Too many requests'),
               })
@api_view(['post'])
@parse_request_data(SendVerificationLinkRequestSerializer)
def send_verification_link(request, data):
    user = User.objects.filter(all_emails__email=data['email']).first()
    if not user: raise NotFound()
    login_code = LoginCode.make(user)
    email_text(user.email, 'Link pro (pře)nastavení hesla, platný jednu hodinu',
               f'{settings.FULL_HOSTNAME}/reset_password'
               f'?email={user.email}'
               f'&code={login_code.code}'
               f'&password_exists={user.has_usable_password()}')

    return Response(status=HTTP_204_NO_CONTENT)


@extend_schema(request=ResetPasswordRequestSerializer,
               responses={
                   200: TokenResponse,
                   404: OpenApiResponse(description='User with email not found'),
                   429: OpenApiResponse(description='Too many requests'),
               })
@api_view(['post'])
@parse_request_data(ResetPasswordRequestSerializer)
def reset_password(request, data):
    user = User.objects.filter(all_emails__email=data['email']).first()
    if not user: raise NotFound()
    validate_password(data['password'], user)
    LoginCode.is_valid(user, data['code'])
    user.set_password(data['password'])
    user.save()

    return login_and_return_token(request, user)