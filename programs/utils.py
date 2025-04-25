from django.db import models

import random
import string

def generate_ch_id():
    """"
    Generate a random ID with the prefix 'ch-' followed by 8 random alphanumeric characters.
    """
    prefix = "ch-"
    random_part = ''.join(random.choices(
        string.ascii_lowercase + string.digits, 
        k=8
    ))
    return f"{prefix}{random_part}"


class CustomIDField(models.CharField):
    """
    Custom field to generate a unique ID for each instance of the model.
    The ID is generated using the `generate_ch_id` function.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            value = generate_ch_id()
            while model_instance.__class__.objects.filter(**{self.attname: value}).exists():
                value = generate_ch_id()
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)