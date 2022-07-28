from rest_framework import serializers
from .models import Post, Comment, Like
from user.models import User
from user.serializers import UserSerializer


class FilterCommentListSerializer(serializers.ListSerializer):


    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AuthorSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", 'profile']
        depth = 1

        extra_kwargs = {"profile": {"read_only": True}}


class LikesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"

        extra_kwargs = {"author": {"read_only": True}}


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("post", "text", "parent")


class ListCommentSerializer(serializers.ModelSerializer):

    text = serializers.SerializerMethodField()
    children = RecursiveSerializer(many=True)
    user = AuthorSerializer(read_only=True)

    def get_text(self, obj):
        if obj.deleted:
            return None
        return obj.text

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = "id post user  text  created_date update_date deleted children".split()


class PostSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    comments = ListCommentSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = "id user image  author text comments view_count".split()


class ListPostSerializer(serializers.ModelSerializer):
    user = AuthorSerializer

    class Meta:
        model = Post
        fields = "author_id create_date author text  comments_count".split()


class LikesDetailedSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"

        extra_kwargs = {"author": {"read_only": True}}
