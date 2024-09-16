from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from core import simple_send_mail, logger


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str, **extra_fields):
        if not phone_number:
            raise ValueError("You should enter PhoneNumber")

        if not password:
            raise ValueError("You should enter Password")
        
        # if 'email' in extra_fields.keys(): # For set optional email
        # extra_fields['email'] = self.normalize_email(extra_fields['email'])
        if extra_fields.get('email') is not None:
            extra_fields["email"] = self.normalize_email(extra_fields["email"])

        user = self.model(phone_number=phone_number, **extra_fields)

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=12,verbose_name="شماره تلفن",unique=True)
    full_name = models.CharField("نام", max_length=150, null=True)
    email = models.EmailField("آدرس ایمیل", unique=True, null=True, blank=True)
    is_active = models.BooleanField("آیا فعال است ؟",default=True)
    is_admin = models.BooleanField("آیا ادمین است ؟",default=False)
    joined_at = models.DateTimeField("تاریخ پیوستن", auto_now_add=True)

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def send_email(self, subject: str, msg: str) -> bool:
        try:
            simple_send_mail(subject, msg, self.email)
            return True
        except Exception as e:
            logger.warning(f"can't send email for {self.pk}-{self.email} because {e}")
            return False
    
    @property
    def is_staff(self):
        return self.is_admin

    # REQUIRED_FIELDS = ["email"]