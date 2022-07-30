from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets

from rest_framework.views import Response
from django.shortcuts import get_object_or_404

from .base import IsAuthor
from .serializers import *
from .models import *
from .base import UpdateOwn

from rest_framework import permissions

from .models import Post, Comment
from .serializers import PostSerializer, ListCommentSerializer




class PostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer


class CommentsView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListCommentSerializer
    permission_classes_by_action = [IsAuthor]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()



class LikeViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikesSerializer
    filterset_fields = ("author__id",)
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        post_id = request.data["post"]
        post = get_object_or_404(Post, pk=post_id)
        new_like, _ = Like.objects.get_or_create(author=request.user, post=post)
        serializer = self.serializer_class(new_like).data
        return Response(data=serializer, status=status.HTTP_201_CREATED)


