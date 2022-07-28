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
from .base import CreateUpdateDestroy, CreateRetrieveUpdateDestroy

from .base import IsAuthor
from .models import Post, Comment
from .serializers import PostSerializer, ListPostSerializer, CreateCommentSerializer



class FeedApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PostSerializer

    def get(self, request, pk=None):
        follows = User.objects.get(user=request.user).follows.all()
        feed_queryset = Post.objects.filter(author__id__in=follows)
        data = self.serializer_class(
            feed_queryset, many=True, context={"request": request}
        ).data

        return Response(data=data)




class PostView(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer








class CommentsView(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer


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


class LikedApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        liked_posts = Post.objects.filter(likes__author__id=request.user.id)
        serializer_data = self.serializer_class(
            liked_posts, many=True, context={"request": request}
        ).data

        return Response(data=serializer_data)


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


# class PostComments(APIView):
#     authentication_classes = [TokenAuthentication]
#     serializer_class = CommentSerializer
#
#     def get(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         comments_data = self.serializer_class(
#             post.comments, many=True, context={"request": request}
#         ).data
#
#         return Response(data=comments_data)
