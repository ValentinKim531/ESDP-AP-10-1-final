import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from accounts.models import Account
from api.serializers import NewsSerializer
from webapp.models import News, Cities, Image


class NewsSimpleView(GenericAPIView):

    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        try:
            objects = News.objects.all()
        except ObjectDoesNotExist:
            Response({"error": "Новости отсутствуют"})
        else:
            serializer = NewsSerializer(objects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            photo_list = data.get('photo')
            data.pop('photo')
            data['cities'] = Cities.objects.get(id=data.get('cities'))
            data['user'] = Account.objects.get(id=data.get('user'))
            news = News.objects.create(**data)
            for photo_id in photo_list:
                news.photo.add(Image.objects.get(id=photo_id))
                news.save()
            return Response({"create": "успешно создано"})
        except Exception:
            response = Response({'errors': "ошибка"})
            response.status_code = 400
            return response


class NewsApiView(GenericAPIView):

    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        try:
            objects = get_object_or_404(News, pk=kwargs.get("pk"))
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        serializer = NewsSerializer(objects)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        objects = get_object_or_404(News, pk=kwargs.get("pk"))
        serializer = NewsSerializer(objects, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = Response({'errors': serializer.errors})
            response.status_code = 400
            return response

    def delete(self, request, *args, **kwargs):
        try:
            objects = get_object_or_404(News, pk=kwargs.get("pk"))
            objects.delete()
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        return Response({f"delte - {kwargs.get('pk')}": "мягкое удаление успешно выполнелось"})
