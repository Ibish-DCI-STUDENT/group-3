from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CourseFilteredList(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Course.objects.all()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        instructor = self.request.query_params.get('instructor')
        duration = self.request.query_params.get('duration')

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if instructor is not None:
            queryset = queryset.filter(instructor=instructor)

        if duration is not None:
            queryset = queryset.filter(duration=duration)

        return queryset
