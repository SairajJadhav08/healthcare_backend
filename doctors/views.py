from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor records.
    
    - All authenticated users can view all doctors.
    - Only the creator can update or delete a doctor.
    - All endpoints require JWT authentication.
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()

    def perform_create(self, serializer):
        """Automatically set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Only the creator can update a doctor record."""
        if serializer.instance.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to update this doctor record.")
        serializer.save()

    def perform_destroy(self, instance):
        """Only the creator can delete a doctor record."""
        if instance.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to delete this doctor record.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """Delete a doctor and return confirmation."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Doctor record deleted successfully."},
            status=status.HTTP_200_OK,
        )
