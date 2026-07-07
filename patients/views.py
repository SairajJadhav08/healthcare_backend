from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient records.
    
    - Users can only see and manage patients they created.
    - All endpoints require JWT authentication.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only patients created by the authenticated user."""
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific patient."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        """Delete a patient and return confirmation."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Patient record deleted successfully."},
            status=status.HTTP_200_OK,
        )
