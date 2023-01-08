from django.conf import settings
from django.db.models import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        err_message = f'Ошибка зачисления/перевода: ' \
                      f'студентов на курсе не должно быть больше {settings.MAX_STUDENTS_PER_COURSE}'

        method = self.context['request'].method

        if (method == 'POST') and len(data['students']) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(detail=err_message)

        if (method == 'PATCH' or method == 'PUT') and data.get('students'):
            count_students_on_course = Course.objects.filter(id=self.instance.id).annotate((Count('students')))
            quantity = len(data['students']) + count_students_on_course[0].students__count
            if quantity > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(detail=err_message)
        return data

