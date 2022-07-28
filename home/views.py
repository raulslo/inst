from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets

from rest_framework.views import Response
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from .permissions import UpdateOwn

from rest_framework import permissions, generics

from .base import IsAuthor
from .models import Post, Comment
from .serializers import PostSerializer, ListCommentSerializer




class PostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer


class CommentsView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, UpdateOwn]
    serializer_class = ListCommentSerializer

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


class PostLikes(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = LikesSerializer

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post_data = PostSerializer(post, context={"request": request}).data
        likes_data = self.serializer_class(
            post.likes, many=True, context={"request": request}
        ).data

        return Response(data={"likes": likes_data, "is_liked": post_data["is_liked"]})
