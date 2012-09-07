from django.dispatch import Signal

user_modify_gallery = Signal(providing_args=['gallery'])
