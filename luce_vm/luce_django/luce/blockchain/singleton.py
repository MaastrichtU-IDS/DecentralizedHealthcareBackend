from django.db import models
from abc import abstractmethod


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

    contract_name = models.CharField(max_length=100,
                                     null=True,
                                     blank=True,
                                     default="")

    class Meta:
        abstract = True

    @abstractmethod
    def deploy(self):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if created:
            print(f"{obj.contract_name} Singleton instance created.")
            obj.deploy()
        else:
            print(
                f"{obj.contract_name} Singleton ({obj.contract_address}) instance loaded."
            )
        return obj