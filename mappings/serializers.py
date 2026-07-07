from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for creating patient-doctor mappings."""

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """Check that the mapping doesn't already exist."""
        if PatientDoctorMapping.objects.filter(
            patient=data['patient'],
            doctor=data['doctor'],
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )
        return data


class PatientDoctorMappingDetailSerializer(serializers.ModelSerializer):
    """Serializer for reading patient-doctor mappings with nested details."""
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'created_at']
