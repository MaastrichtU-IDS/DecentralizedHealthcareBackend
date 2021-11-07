from django import forms

from datastore.models import Dataset

class DatasetModelForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'description', 'file', 'license']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = Dataset.objects.filter(title__iexact=title)
        # exclude current instance from qs to allow same title during update
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # pk is primary key, same as id
        if qs.exists():
            raise forms.ValidationError("This title has already been used.")
        return title