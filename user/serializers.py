from rest_framework import serializers

from .models import User, UserProfile, Follower


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(min_length=8, write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    class Meta:
        model = User
        fields = "first_name last_name username email password password2".split()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.password == password:
                    return user
                else:
                    raise serializers.ValidationError("Incorrect password")
            else:
                raise serializers.ValidationError("User does not exist")

    class Meta:
        model = User
        fields = "email password".split()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSerializer
        fields = "id  username  photo".split()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username password email profile".split()


class ListFollowerSerializer(serializers.ModelSerializer):
    subscribers = UserFollowerSerializer(many=True, read_only=True)

    class Meta:
        model = Follower
        fields = "__all__"
