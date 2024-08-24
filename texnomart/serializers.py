from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from texnomart.models import Category, Image, Product, Comment, ProductAttribute,Attribute,AttributeValue

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary', 'product', 'category']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ()
        # fields = ['id','attribute_name']

class AttributevalueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        exclude = ()

      


class ProductSerializer(serializers.ModelSerializer):
    # categories= CategoryModelSerializer(many=False, read_only=True)
    # category_name = serializers.CharField(source='category.category_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter(product=instance).values_list('key_id', 'key__attribute_name',
                                                                                   'value_id',
                                                                                   'value__attribute_value')

        characters = [
            {
                'attribute_id': key_id,
                'attribute_name': key_name,
                'attribute_value_id': value_id,
                'attribute_value': value_name
            }
            for key_id, key_name, value_id, value_name in attributes]
        return characters
    
    def get_avg_rating(self, obj):
        avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0

    def get_comments_count(self, instance):
        count = Comment.objects.filter(product=instance).count()
        return count

    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False

    def get_all_images(self, instance):
        images = Image.objects.all().filter(product=instance)
        all_images = []
        request = self.context.get('request')

        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))

        return all_images

    def get_primary_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        exclude = ()
class ProductAttributeSerializer(serializers.ModelSerializer): 
    products = serializers.CharField(source='product.product_name')
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter().values_list('key_id', 'key__attribute_name',
                                                                                   'value_id',
                                                                                   'value__attribute_value')

        characters = [
            {
                'attribute_id': key_id,
                'attribute_name': key_name,
                'attribute_value_id': value_id,
                'attribute_value': value_name
            }
            for key_id, key_name, value_id, value_name in attributes]
        return characters
    class Meta:
        model = ProductAttribute
        fields = ['id','products','attributes']
        # exclude = ()  
 
class CategoryModelSerializer(serializers.ModelSerializer):
    products = serializers.CharField( read_only=True,source='product.product_name')
    # images = ImageSerializer(many=True, read_only=True, source='category_images')
    category_image = serializers.SerializerMethodField(method_name='foo')
    
    



    def foo(self, instance):
        image = Image.objects.filter(category=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None

    class Meta:
        model = Category
        # exclude =()
        fields = ['id', 'category_name', 'slug', 'category_image', 'products']

class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only = True)
    username = serializers.CharField(read_only = True)
    password = serializers.CharField(read_only = True)

    class Meta:
        model = User
        fields = ['id','username','password']       
class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name",
                  "last_name", "email", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        passowrd2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(passowrd)
        user.save()
        Token.objects.create(user=user)
        return user

    