from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer, PatientDoctorMappingDetailSerializer
from patients.models import Patient


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def mapping_list_create(request):
    """
    POST: Assign a doctor to a patient.
    GET: Retrieve all patient-doctor mappings.
    """
    if request.method == 'POST':
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            # Verify the patient belongs to the authenticated user
            patient = serializer.validated_data['patient']
            if patient.created_by != request.user:
                return Response(
                    {"error": "You can only create mappings for your own patients."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            return Response(
                {
                    "message": "Doctor assigned to patient successfully.",
                    "mapping": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # GET: Return all mappings
    mappings = PatientDoctorMapping.objects.all()
    serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mapping_by_patient(request, patient_id):
    """Get all doctors assigned to a specific patient."""
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    mappings = PatientDoctorMapping.objects.filter(patient=patient)
    serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def mapping_delete(request, id):
    """Remove a doctor from a patient."""
    try:
        mapping = PatientDoctorMapping.objects.get(id=id)
    except PatientDoctorMapping.DoesNotExist:
        return Response(
            {"error": "Mapping not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Verify the patient belongs to the authenticated user
    if mapping.patient.created_by != request.user:
        return Response(
            {"error": "You do not have permission to delete this mapping."},
            status=status.HTTP_403_FORBIDDEN,
        )

    mapping.delete()
    return Response(
        {"message": "Doctor removed from patient successfully."},
        status=status.HTTP_200_OK,
    )
