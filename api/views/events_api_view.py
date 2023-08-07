from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.generics import GenericAPIView

from accounts.models import Account
from api.serializers import EventsSerializer, UserBookedSerializer
from webapp.models import Events, Cities, TypeEvents, Image, UserBooked


class EventsSimpleView(GenericAPIView):

    serializer_class = EventsSerializer

    def get(self, request, *args, **kwargs):
        try:
            events = Events.objects.all()
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        else:
            serializer = EventsSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            data['photo'] = Image.objects.get(id=data.get('photo'))
            data['cities'] = Cities.objects.get(id=data.get('cities'))
            data['type_events'] = TypeEvents.objects.get(id=data.get('type_events'))
            data['sponsor'] = Account.objects.get(id=data.get('sponsor'))
            events = Events.objects.create(**data)
            return Response({"create": "успешно создано"})
        except Exception:
            response = Response({'errors': "ошибка"})
            response.status_code = 400
            return response


class EventApiView(GenericAPIView):

    serializer_class = EventsSerializer

    def get(self, request, *args, **kwargs):
        try:
            objects = get_object_or_404(Events, pk=kwargs.get("pk"))
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        serializer = EventsSerializer(objects)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        objects = get_object_or_404(Events, pk=kwargs.get("pk"))
        serializer = EventsSerializer(objects, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = Response({'errors': serializer.errors})
            response.status_code = 400
            return response

    def delete(self, request, *args, **kwargs):
        try:
            objects = get_object_or_404(Events, pk=kwargs.get("pk"))
            objects.delete()
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        return Response({f"delte - {kwargs.get('pk')}": "мягкое удаление успешно выполнелось"})


class EventsBookedSimpleView(GenericAPIView):

    serializer_class = UserBookedSerializer

    def get(self, request, *args, **kwargs):
        try:
            events = UserBooked.objects.all()
        except ObjectDoesNotExist:
            Response({"error": "введите существующий pk"})
        else:
            serializer = UserBookedSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            data['event'] = Events.objects.get(id=data.get('event'))
            data['resident'] = Account.objects.get(id=data.get('resident'))
            events = UserBooked.objects.create(**data)
            return Response({"create": "успешно создано"})
        except Exception:
            response = Response({'errors': "ошибка"})
            response.status_code = 400
            return response