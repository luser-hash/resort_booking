from datetime import date
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.models import ProviderProfile
from .models import RoomBooking
from .services import auto_complete_finished_bookings
from .serializer import RoomBookingSerializer, RoomBookingCreateSerializer, BookingDetailSerializer
from accounts.permissions import IsGuest, IsProvider, IsAdmin


# Read only list for all room bookings
class RoomBookingListAPIView(generics.ListAPIView):
    queryset = RoomBooking.objects.all().order_by('-created_at')
    serializer_class = RoomBookingSerializer


class RoomBookingCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomBookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # run default create first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Now re-serialize with detail serializer
        from .serializer import BookingDetailSerializer
        detail = BookingDetailSerializer(booking)

        headers = self.get_success_headers(detail.data)
        return Response(detail.data, status=status.HTTP_201_CREATED, headers=headers)


class MyRoomBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    # only logged in user can see their bookings

    # get_queryset narrows to bookings of 'request.user'
    def get_queryset(self):
        # auto complete finished bookings on each call
        auto_complete_finished_bookings()
        return RoomBooking.objects.filter(
            user=self.request.user
        ).order_by('-created_at') 


class ProviderBookingsAPIView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        # auto complete finished bookings on each call
        auto_complete_finished_bookings()
        provider_id = self.kwargs['provider_id']
        return RoomBooking.objects.filter(
            provider_id=provider_id
        ).order_by('-created_at')


class CancelRoomBookingAPIView(APIView):
    # allows only authenticated users to cancel their bookings
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(RoomBooking, id=booking_id)

        # OwnerShip check
        if booking.user != request.user:
            return Response(
                {'detail': 'Not authorized to cancel this booking.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # status rule, only pending or confirmed bookings can be cancelled
        if booking.status not in ['PENDING', 'CONFIRMED']:
            return Response(
                {'detail': 'Only pending or confirmed bookings can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Date rule - cannot cancel on or after check-in date
        if date.today() >= booking.check_in:
            return Response(
                {'detail': 'Cannot cancel booking on or after check-in date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Finally if all rules passed cancel the booking
        booking.status = 'CANCELLED'
        booking.save()

        # Return the updated booking 
        serialzer = RoomBookingSerializer(booking)
        return Response(serialzer.data, status=status.HTTP_200_OK)


class ConfirmRoomBookingAPIView(APIView):
    # only the authenticated provider can confirm bookings
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def post(self, request, booking_id):
        booking = get_object_or_404(RoomBooking, id=booking_id)

        # get the provider profile of the logged in user
        try:
            provider_profile = request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            return Response(
                {'detail': 'Only providers can confirm bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # OwnerShip check - only provider can confirm
        if booking.provider != provider_profile:
            return Response(
                {'detail': 'Not authorized to confirm this booking.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Status rule - only pending bookings can be confirmed
        if booking.status != 'PENDING':
            return Response(
                {'detail': 'Only pending bookings can be confirmed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Finally if all rules passed confirm the booking
        booking.status = 'CONFIRMED'
        booking.save()

        # Return the updated booking
        seraializer = RoomBookingSerializer(booking)
        return Response(seraializer.data, status=status.HTTP_200_OK)


class RejectRoomBookinAPIView(APIView):
    # onlu authenticated provider can reject bookings
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def post(self, request, booking_id):
        # Get the booking object
        booking = get_object_or_404(RoomBooking, id=booking_id)

        # Get provider profile of logged in user
        try:
            provider_profile = request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            return Response(
                {'detail': 'Only providers can reject bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Ownership check - only provider can reject
        if booking.provider != provider_profile:
            return Response(
                {'detail': 'Not authorized to reject this booking.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # only pending bookings can be rejected
        if booking.status != 'PENDING':
            return Response(
                {'detail': 'Only pending bookings can be rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Finally if all rules passed reject the booking
        booking.status = 'REJECTED'
        booking.save()

        # Return the updated booking
        serializer = RoomBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



    