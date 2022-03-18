from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Teacher
from apps.students.models import Student, Assignment
from .serializers import TeacherAssignmentSerializer

# Create your views here.


class AssignmentView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        print('update request')
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id
        print(request.data)

        try:
            assignment = Assignment.objects.get(
                pk=request.data['id'])
        except Assignment.DoesNotExist:
            return Response(
                data={'error': 'Assignment does not exist/permission denied'},
                status=status.HTTP_400_BAD_REQUEST
            )
        print('cool')

        request.data["state"] = assignment.state
        # if 'grade' in request.data:
        #     assignment.grade = request.data['grade']


        serializer = self.serializer_class(
            assignment, data=request.data, partial=True)
        if serializer.is_valid():
            if not assignment.teacher.id == teacher.id:
                return Response(data={"non_field_errors": ['Teacher cannot grade for other teacher''s assignment']}, status=status.HTTP_400_BAD_REQUEST)
            print(serializer.validated_data['state'])
            serializer.validated_data['state'] = 'GRADED'
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
