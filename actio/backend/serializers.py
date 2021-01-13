from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin


class CourseCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('category', )


class CourseSubCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseSubcategory
        fields = ('subcategory', )


class CoachSerializer(ModelSerializer):
    class Meta:
        model = Coach
        fields = ('display_name', )


class ActioSessionSerializer(SerializerExtensionsMixin, ModelSerializer):
    class Meta:
        model = ActioSession
        fields = ('id', 'course_category', 'course_subcategory', 'coach', 'conducted_on', 'start_time', 'end_time',
                  'session_status')

        expandable_fields = dict(
            course_category=dict(
                serializer=CourseCategorySerializer,
                id_source='course_category.pk'
            ),
            course_subcategory=dict(
                serializer=CourseSubCategorySerializer,
                id_source='subcategory.pk',
            ),
            coach=dict(
                serializer=CoachSerializer,
                id_source='coach.pk'
            )
        )