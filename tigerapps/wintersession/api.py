from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from wintersession.models import Student, Course, Registration


class InstructorNameField(serializers.RelatedField):
    def to_native(self, value):
        return value.full_name()


class CourseSerializer(serializers.ModelSerializer):
    instructors = InstructorNameField(many=True)
    sections = serializers.Field(source='all_section_ids')

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'min_enroll', 'max_enroll', 'cancelled', 'room', 'instructors', 'sections')


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Course.objects.exclude(courseID__regex=r'^.*\.[^a].*$')
    serializer_class = CourseSerializer


class SectionSerializer(serializers.ModelSerializer):
    schedule = serializers.Field(source='this_section.as_dict')
    blocks = serializers.Field(source='blocks')

    class Meta:
        model = Course
        fields = ('id', 'blocks', 'schedule')


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Course.objects.all()
    serializer_class = SectionSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(source='course')

    class Meta:
        model = Registration
        fields = ('id', 'section')


class RegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        student = Student.objects.get(netID=self.request.user)
        return student.registration_set.all()


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'registrations', RegistrationViewSet, base_name='registration')
