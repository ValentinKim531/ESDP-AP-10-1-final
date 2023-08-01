import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from api.serializers import RoleSerializer
from accounts.models import Role


class PrivilegesApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            privileges_list = Role.PRIVILEGES_CHOICES
        except ObjectDoesNotExist:
            response = Response({"error": "Данная операция не доступна"})
            response.status_code = 400
            return response
        else:
            return Response(privileges_list, status=status.HTTP_200_OK)

class RoleApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            role_list = Role.objects.all()
        except ObjectDoesNotExist:
            response = Response({"error": "Данная операция не доступна"})
            response.status_code = 400
            return response
        else:
            serializer = RoleSerializer(role_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            serializer = RoleSerializer(data=data)
            if serializer.is_valid():
                Role.objects.create(**data)
                return Response({"create": "Запрос успешно создан"})
        except Exception:
            response = Response({'errors': "ошибка"})
            response.status_code = 400
            return response


class RoleDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            sub_level_detail = get_object_or_404(Role, pk=kwargs.get("pk"))
            serializer = RoleSerializer(sub_level_detail)
        except ObjectDoesNotExist:
            response = Response({"error": "Данная операция не доступна"})
            response.status_code = 400
            return response
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            object = get_object_or_404(Role, pk=kwargs.get('pk'))
            serializer = RoleSerializer(object, data=data)
            if serializer.is_valid():
                serializer.update(instance=object, validated_data=data)
                return Response(serializer.data)
        except Exception:
            response = Response({'errors': "ошибка"})
            response.status_code = 400
            return response

    def delete(self, request, *args, **kwargs):
        try:
            objects = get_object_or_404(Role, pk=kwargs.get("pk"))
            objects.delete()
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        return Response({f"delete - {kwargs.get('pk')}": "удаление успешно выполнелось"})
