from datetime import datetime, date

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from . import models
from . import serializers
from .services import get_available_rooms_for_model, search_availability_stay


class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer


class HotelRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HotelRoom.objects.all()
    serializer_class = serializers.HotelRoomSerializer


class ResortRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.ResortRoom.objects.all()
    serializer_class = serializers.ResortRoomSerializer


class ResorTListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Resort.objects.all()
    serializer_class = serializers.ResortSerializer


class HomeStayListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HomeStay.objects.all()
    serializer_class = serializers.HomeStaySerializer


class HomeStayRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HomeStayRoom.objects.all()
    serializer_class = serializers.HomeStayRoomSerializer


# Returns available rooms across hotel /resorts/ homestay for a date range. 
class AvailableRoomsAPIView(APIView):
    # Availablity engine for any room model exposed as one API endpoint.
    # GET /api/listings/rooms/available/?check_in=2024-10-01&check_out=2024-10-05&room_type=hotelroom|resortroom|homestayroom 

    # Use this map to get model and serializer based on room_type param
    ROOM_TYPE_MAP = {
        'hotel': (models.HotelRoom, serializers.HotelRoomSerializer),
        'resort': (models.ResortRoom, serializers.ResortRoomSerializer),
        'homestay': (models.HomeStayRoom, serializers.HomeStayRoomSerializer),
    }

    def get(self, request):
        # reading query params
        check_in_str = request.query_params.get('check_in')
        check_out_str = request.query_params.get('check_out')
        room_type = request.query_params.get('room_type')  # optional

        # validate dates
        if not check_in_str or not check_out_str:
            raise ValidationError('Check in and check out params are required')
        
        # parse dates
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('Date must be in YYYY-MM-DD format')
        
        # Basic rules
        if check_out <= check_in:
            raise ValidationError('Check out must be after check in')
        
        if check_in < date.today():
            raise ValidationError('Check in date cannnot be in past!')
        
        result = []
        
        # helper function to add rooms of a specific type
        def add_rooms_for(label, model, serializer_class):
            qs = get_available_rooms_for_model(model, check_in, check_out)
            for room in qs:
                data = serializer_class(room).data
                data['room_type'] = label  # so frontend knows which type
                result.append(data)

        # if specific room_type given fetch only that model
        if room_type:
            room_type = room_type.lower()
            if room_type not in self.ROOM_TYPE_MAP:
                raise ValidationError('Invalid room type!')
            
            model, serializer_class = self.ROOM_TYPE_MAP[room_type]
            add_rooms_for(room_type, model, serializer_class)
        else:
            # no room type, return all types
            for label, (model, serializer_class) in self.ROOM_TYPE_MAP.items():
                add_rooms_for(label, model, serializer_class)

        return Response(result)


# Api View for searching rooms. 
class SearchStaysAPIView(APIView):
    """
    For given check-in, check-out dates and stay types and city it searches and 
    respond back to the frontend. 
    """
    def get(self, request):
        check_in_str = request.query_params.get('check_in')
        check_out_str = request.query_params.get('check_out')
        room_type = request.query_params.get('room_type')
        city = request.query_params.get('city')

        if not check_in_str or not check_out_str:
            raise ValidationError('Check in and check out are required!')
        
        # parse dates
        try:
            check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Dates must be in YYYY-MM-DD format.")
        
        # basic rules
        if check_out <= check_in:
            raise ValidationError("check_out must be after check_in.")
        if check_in < date.today():
            raise ValidationError("check_in cannot be in the past.")
        
        # run core search
        try:
            stays = search_availability_stay(check_in, check_out, room_type, city)
        except ValueError as e:
            raise ValidationError(str(e))
        
        return Response(stays)
