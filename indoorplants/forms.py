from django import forms
from indoorplants.models import PlantType

       
class AddPlantTypeForm(forms.ModelForm):

    class Meta:
        model = PlantType
        fields = '__all__'
        exclude = ['author']
        widgets = {
        'name' : forms.TextInput(attrs = {'placeholder': 'Scientific Name'}), 
        }

class EditPlantTypeImage(forms.ModelForm):

    class Meta:
        model = PlantType
        fields = ('photo',)
        