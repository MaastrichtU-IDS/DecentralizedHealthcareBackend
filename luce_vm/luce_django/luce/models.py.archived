# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsCause(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    ethereum_private_key = models.CharField(max_length=255, blank=True, null=True)
    ethereum_public_key = models.CharField(max_length=255, blank=True, null=True)
    goal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'accounts_cause'


class AccountsUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    active = models.BooleanField()
    admin = models.BooleanField()
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    ethereum_private_key = models.CharField(max_length=255, blank=True, null=True)
    ethereum_public_key = models.CharField(max_length=255, blank=True, null=True)
    staff = models.BooleanField()
    user_type = models.IntegerField()
    is_approved = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DatastoreDataset(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=120)
    owner_address = models.CharField(max_length=180)
    license = models.IntegerField()
    timestamp = models.DateTimeField()
    updated = models.DateTimeField()
    file = models.CharField(max_length=100, blank=True, null=True)
    contract_address = models.CharField(max_length=180)
    published = models.BooleanField()
    created_by = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datastore_dataset'


class DatastoreDatasetAccessGranted(models.Model):
    dataset = models.ForeignKey(DatastoreDataset, models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datastore_dataset_access_granted'
        unique_together = (('dataset', 'user'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class SearchSearchquery(models.Model):
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_searchquery'
