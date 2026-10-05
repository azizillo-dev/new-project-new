from django.db import models
from django.contrib.auth.models import AbstractUser
from baseapp.models import BaseModel
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
CUSTOMER, SELLER = ('customer', 'seller')


class CustomUser(BaseModel, AbstractUser):

    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE),
    )

    ROLE = (
        (CUSTOMER, CUSTOMER),
        (SELLER, SELLER)
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    auth_type = models.CharField(max_length=9, choices=AUTH_TYPE)
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default=NEW)
    role = models.CharField(max_length=20, choices=ROLE, default=CUSTOMER)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)


class Verify(BaseModel):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='codes')
    expire_time = models.DateTimeField()
    used = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=30, choices=CustomUser.AUTH_TYPE)

    def __str__(self):
        return f"Salom, sizning tasdiqlash codingiz: {self.code} | user: {self.user.username}"
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.auth_type == VIA_EMAIL:
                self.expire_time = timezone.now() + timedelta(minutes=settings.EMAIL_EXPIRATION_TIME)
            elif self.auth_type == VIA_PHONE:
                self.expire_time = timezone.now() + timedelta(minutes=settings.PHONE_EXPIRATION_TIME)
        super().save(*args, **kwargs)


    
          





