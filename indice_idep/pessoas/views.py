from django.shortcuts import render

# Create your views here.
from pessoas.api.serializers import UserSerializer
from pessoas.models import Servidores, ServidorUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class LoginView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        # by default attempts username / passsword combination
        response = super(LoginView, self).post(request, *args, **kwargs)
        # token = response.data['token']  # don't use this to prevent errors
        # below will return null, but not an error, if not found :)
        res = response.data
        token = res.get('token')

        # token ok, get user
        if token:
            user = jwt_decode_handler(token)  # already json - don't serialize
        else:
            req = request.data
            rf = req.get('rf')
            password = req.get('cpf')
            anonasc = req.get('anonasc')

            if rf is None or password is None or anonasc is None:
                return Response({'success': False,
                                 'message': 'Missing or incorrect credentials',
                                 'data': req},
                                status=status.HTTP_400_BAD_REQUEST)

            # email exists in request, try to find user
            try:
                servidor = ServidorUser.objects.get(rf=int(rf), password=password, ano_nasc=int(anonasc))
            except:
                return Response({'success': False,
                                 'message': 'User not found',
                                 'data': req},
                                status=status.HTTP_404_NOT_FOUND)

            payload = jwt_payload_handler(servidor)
            token = jwt_encode_handler(payload)
            user = UserSerializer(servidor).data

        return Response({'success': True,
                         'message': 'Successfully logged in',
                         'token': token,
                         'user': user},
                        status=status.HTTP_200_OK)
