from django.db import models


class SingletonModel(models.Model):
    """
    An abstract base class for creating singleton models in Django.
    """
    class Meta:
        abstract = True  # Declare this as an abstract class

    def save(self, *args, **kwargs):
        """
        Override the save method to set the primary key to 1. This ensures that 
        only one instance of the singleton model will exist in the database.
        """
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        A class method to get the singleton instance or create one if it does 
        not exist.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SingletonContractModel(SingletonModel):
    contract_address = models.CharField(max_length=42,
                                        null=True,
                                        blank=True,
                                        default="0x0")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if created:
            print("Singleton instance created.")
            obj.deploy()
        else:
            print("Singleton instance loaded.")
        return obj