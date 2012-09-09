from django.dispatch import Signal

user_modify_gallery = Signal(providing_args=['gallery'])
user_delete_photo = Signal(providing_args=['gallery','index'])
