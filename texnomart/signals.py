import os
import json
from django.db.models.signals import post_save,post_delete, pre_save,pre_delete
from texnomart.models import Category,Product
from django.dispatch import receiver
from config.settings import BASE_DIR
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL



@receiver(pre_delete, sender=Category)
def pre_delete_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR,'texnomart/delete_categories',f'category_{instance.id}.json')

    category_data = {
        'id' : instance.id,
        'category_name' : instance.category_name ,
        'slug' : instance.slug
    }


    with open(file_path,'w') as json_file :
        json.dump(category_data,json_file,indent=4)

@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR,'texnomart/delete_products',f'product_{instance.id}.json')

    product_data = {
        'id' : instance.id,
        'product_name' : instance.product_name ,
        'slug' : instance.slug,
        'description': instance.description,
        'price': instance.price,
        'quantity' : instance.quantity,
        'discount' : instance.discount
    }


    with open(file_path,'w') as json_file :
        json.dump(product_data,json_file,indent=4)

@receiver(post_save, sender=Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print('Category created ')
        subject = 'Category created'
        message = f' Category {instance.category_name } Admin tomonidan yaratildi'
        from_email = DEFAULT_FROM_EMAIL
        to = 'abdurahimovsamir219@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)

    else:
        print('category updated')

@receiver(post_delete, sender=Category)
def post_delete_category( sender,instance, **kwargs):
    print(f'About to delete category: {instance.category_name}')
    if post_delete:
        print('Category delete ')
        subject = 'Category delete'
        message = f' Category {instance.category_name } Admin tomonidan ochirildi'
        from_email = DEFAULT_FROM_EMAIL
        to = 'abdurahimovsamir219@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)

    else:
        print('Category updated')

@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product created ')
        subject = 'Product created'
        message = f' Product {instance.product_name } Admin tomonidan yaratildi'
        from_email = DEFAULT_FROM_EMAIL
        to = 'abdurahimovsamir219@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)

    else:
        print('Product updated')


@receiver(post_delete, sender=Product)
def post_delete_product( sender,instance, **kwargs):
    print(f'About to delete product: {instance.product_name}')
    if post_delete:
        print('Product delete ')
        subject = 'Product delete'
        message = f' Product {instance.product_name } Admin tomonidan ochirildi'
        from_email = DEFAULT_FROM_EMAIL
        to = 'abdurahimovsamir219@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)

    else:
        print('Product updated')