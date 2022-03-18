from rest_framework import serializers
from apps.students.models import Assignment


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment Serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        if "content" in attrs:
            raise serializers.ValidationError(
                "Teacher cannot change the content of the assignment"
            )
        if "student" in attrs:
            raise serializers.ValidationError(
                "Teacher cannot change the student who submitted the assignment"
            )
        
        # if 'teacher' in attrs:
        #     if self.teacher != attrs['teacher']:
        #         raise serializers.ValidationError(
        #             "Teacher cannot grade for other teacher''s assignment"
        #         )

        print(self)
        print(attrs['teacher'])

        if 'state' in attrs:
            if attrs["state"] == "DRAFT":
                raise serializers.ValidationError(
                    "SUBMITTED assignments can only be graded"
                )
            if attrs["state"] == "GRADED":
                raise serializers.ValidationError(
                    "GRADED assignments cannot be graded again"
                )
            # if attrs["state"] == "SUBMITTED":
            #     raise serializers.ValidationError(
            #         "Cannot modify state to submitted"
            #     )
        # if 'grade' in attrs:
        #     self.grade = 'GRADED'

        if self.partial:
            return attrs

        return super().validate(attrs)
