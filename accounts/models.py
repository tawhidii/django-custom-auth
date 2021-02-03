from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, first_name,last_name,is_staff,is_superuser,password,dob=None,gender=None,email=None,phone_number=None,**kwargs):
        now = timezone.now()

        if not first_name:
            raise ValueError('You must enter your first name')

        if not last_name:
            raise ValueError('You must enter your last name')
        
        if not password:
            raise ValueError('You must enter a password')

        
        email = self.normalize_email(email)

        user = self.model(first_name=first_name, 
                          last_name=last_name,
                          dob=dob,
                          gender=gender,
                          email=email,
                          phone_number=phone_number,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **kwargs)

        user.set_password(password)
        user.save(using=self.db)

        return user

    # create normal user
    def create_user(self,first_name,last_name,dob=None,gender=None,email=None,phone_number=None,password=None,**kwargs):
        return self._create_user(first_name,last_name,False,False,password,dob,gender,email,phone_number,**kwargs)

    #create super user
    def create_superuser(self,first_name,last_name,dob=None,gender=None,email=None,phone_number=None,password=None,**kwargs):
        return self._create_user(first_name,last_name,True,True,password,dob,gender,email,phone_number,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    email = models.EmailField(blank=True,null=True,unique=True)
    phone_number = PhoneNumberField(blank=True,null=True,verbose_name='Contact number')
    dob = models.DateField(auto_now_add=False,verbose_name="Date of Birth")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    GENDER = (
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    )
    age = models.PositiveIntegerField(blank=True,null=True)
    gender = models.CharField(max_length=5,choices=GENDER,blank=True,null=True)
    avatar = models.ImageField(blank=True,null=True,upload_to='avatar/')
    bio = models.CharField(max_length=512,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','dob','phone_number']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        full_name = str(self.first_name +' '+ self.last_name)
        return full_name
    