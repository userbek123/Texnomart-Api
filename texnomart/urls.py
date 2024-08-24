from django.contrib import admin
from django.urls import path,include
from texnomart import views
from rest_framework.routers import DefaultRouter
from texnomart import auth

router = DefaultRouter()

router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('products',views.ProductModelViewSet ,basename='product')

urlpatterns = [
    path('',views.ProductListApiView.as_view(),name='all_products'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),   
    path('products/', views.ProductListApiView.as_view(), name='products'),
    path('images/', views.ImageListApiView.as_view(), name='image_list'),
    path('add-comment/',views.CommentAdd.as_view(),name= 'add_comment'),
    # CATEGORIES
    path('category-detail/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category-add/', views.CategoryAdd.as_view()),
    path('category-change/<slug:slug>/', views.CategoryUpdate.as_view()),
    path('category-delete/<slug:slug>/', views.CategoryDelete.as_view()),
    path('modelviewset/', include(router.urls)),
    # PRODUCTS
    path('products-detail/<int:pk>', views.ProductDetail.as_view()),
    path('product-add/', views.ProductsAdd.as_view()),
    path('product-change/<int:pk>', views.ProductsUpdate.as_view()),
    path('product-delete/<int:pk>', views.ProductsDelete.as_view()),
    # Login
    path('login/',auth.UserLoginAPIView.as_view(),name = 'login'),
    path('register/',auth.UserRegisterAPIView.as_view(), name='register'),
    path('logout/',auth.UserLogoutAPIView.as_view(),name = 'logout'),
    # ATTRIBUTES
    path('attributes-keys/',views.AttributesView.as_view()),
    path('attributes-values/',views.AttributesValueView.as_view()),
    path('product-attributes-values/<int:pk>',views.ProductAttributesView.as_view()),
    
    
]