from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from texnomart.models import Category, Image, Product,Comment,Attribute,AttributeValue,ProductAttribute
from texnomart.serializers import CategoryModelSerializer,ProductSerializer,ImageSerializer,CommentSerializer,AttributeSerializer,AttributevalueSerializer,ProductAttributeSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class CategoryDetailView(APIView):
    def get(self, request,slug):
        categories = get_object_or_404(Category,slug=slug)
        serializers = CategoryModelSerializer(categories, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)      
      
class ProductDetailView(APIView):
    def get(self, request,slug):
        products = get_object_or_404(Product,slug=slug)
        serializers = ProductSerializer(products, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK) 

class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'pk'


class CategoryList(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    serializer_class = CategoryModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fiealds = ('category_name','slug')
    queryset = Category.objects.all()


    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ProductListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes =[JWTAuthentication]
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('product_name','slug')
    queryset = Product.objects.select_related('category').prefetch_related('users_like',).all()
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)        

    

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

class ImageListApiView(APIView):
    def get(self, request):
        images = Image.objects.select_related('product','category').all()
        serializers = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)



class ProductDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Product.objects.all()
        return  queryset

class CommentAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication]
    queryset = Comment.objects.all()

class CategoryAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

class CategoryUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'

class CategoryDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'    

# PRODUCT
class ProductsAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductsUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

class ProductsDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

class AttributesView(APIView):
    def get(self, request,):
        attributes = Attribute.objects.all()
        serializers = AttributeSerializer(attributes, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class AttributesValueView(APIView):
    def get(self, request,):
        attributes = AttributeValue.objects.all()
        serializers = AttributevalueSerializer(attributes, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)    

class ProductAttributesView(APIView):
    # permission_classes = [IsAuthenticated]
    # serializer_class = ProductAttributeSerializer
    # queryset = ProductAttribute.objects.all()
    # lookup_field = 'pk'

    def get(self, request,pk):
        attributes = ProductAttribute.objects.all()
        serializers = ProductAttributeSerializer(attributes, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)  
