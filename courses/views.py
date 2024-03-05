from rest_framework import generics, permissions
from .models import Course, Comment, Rating
from .serializers import CourseSerializer, CommentSerializer, RatingSerializer
from django.shortcuts import get_object_or_404


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseFilteredList(generics.ListAPIView):
    serializer_class = CourseSerializer
    #permission_classes = [permissions.AllowAny]

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


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return Comment.objects.filter(course_id=course_pk)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        serializer.save(user=self.request.user, course=course)

class RatingListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return Rating.objects.filter(course_id=course_pk)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        serializer.save(user=self.request.user, course=course)

class LikeListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        return Rating.objects.filter(course_id=course_pk)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        serializer.save(user=self.request.user, course=course)
