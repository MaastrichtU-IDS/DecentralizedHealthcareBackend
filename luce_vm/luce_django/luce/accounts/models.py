# accounts.models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, gender, age, first_name, last_name, user_type=None, password=None, ethereum_private_key=None, ethereum_public_key=None, contract_address=None, is_staff=False,  is_admin=False):
        """
        Creates and saves a User with the given arguments and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first_name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not password:
        	raise ValueError('Users must have a password')
     
        user = self.model(
            email=self.normalize_email(email),
        )

        user.gender = gender
        user.staff = is_staff
        user.set_password(password)
        user.first_name 	= first_name
        user.last_name 		= last_name
        user.admin = is_admin
        user.ethereum_private_key = ethereum_private_key
        user.ethereum_public_key = ethereum_public_key
        user.user_type = user.user_type
        user.save(using=self._db)
        user.contract_address = contract_address
        user.age = age
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, 
                        ethereum_public_key  = "0x43e196c418b4b7ebf71ba534042cc8907bd39dc9", 
                        ethereum_private_key = "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3"):
        """
        Creates and saves a superuser.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            ethereum_public_key = "0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
            ethereum_private_key = "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3"
        )
        user.staff = True
        user.admin = True
        user.user_type = 3
        user.save(using=self._db)
        return user

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


# Our custom user class
class User(AbstractBaseUser):
	# id, 
	# password and 
	# last_login are automatically inherited AbstractBaseUser
	# The other model fields we define ourselves
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    ethereum_private_key = models.CharField(max_length=255, blank=True, null=True)
    ethereum_public_key = models.CharField(max_length=255, blank=True, null=True)

    # Make these fields compulsory?
    first_name 	= 	models.CharField(max_length=255, blank=True, null=True)
    last_name 	= 	models.CharField(max_length=255, blank=True, null=True)

    # Can use this later to activate certain features only 
    # once ethereum address is associated
    is_approved =  models.BooleanField(default=True, null=True, blank=True) # True for now while developing..

    # user_type is used to know if the user is a Data Provider(0) or a data requester(1)
    user_type = models.IntegerField(
        choices = [(0,"Data Provider"), (1, "Data Requester")]
     )

    # active user? -> can login
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user

    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    #gender of the user
    gender = models.CharField(
        choices=[(0, 'Male'), (1,'Female')],
        max_length=6, 
        null = True
        )
    
    age = models.IntegerField(null = True)

    # Define which field should be the username for login
    USERNAME_FIELD = 'email'

    # USERNAME_FIELD & Password are required by default
    # Add additional required fields here:
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    objects = UserManager()

    # The following default methods are expected to be defined by Django
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    # Properties are based on our custom attributes
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

class Restrictions(models.Model):
    no_restrictions =  models.BooleanField()
    open_to_general_research_and_clinical_care = models.BooleanField()
    open_to_HMB_research = models.BooleanField()
    open_to_population_and_ancestry_research = models.BooleanField()
    open_to_disease_specific = models.BooleanField()

class ConsentContract(models.Model):
    contract_address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restrictions = models.ForeignKey(Restrictions, on_delete=models.CASCADE)




"""

class Cause(models.Model):

    title = models.CharField(max_length=255)
    goal = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    ethereum_private_key = models.CharField(max_length=255, blank=True, null=True)
    ethereum_public_key = models.CharField(max_length=255, blank=True, null=True)
    percentBPS = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)], default=10000)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Donation(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default = 0)



class CauseGroup(models.Model):
    name = models.CharField(max_length=255, default = '')
    description = models.CharField(max_length=255, default = '')
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)



    
class GroupInfo(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    group = models.ForeignKey(CauseGroup, related_name='group', on_delete=models.CASCADE, null = True)
    split = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)])
    
"""