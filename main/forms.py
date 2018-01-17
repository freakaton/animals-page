from django import forms
from main.models import Animal, Post

class Add_animal_form(forms.ModelForm):
    def clean_name(self):
        if Animal.objects.filter(name=self.cleaned_data['name']).count() > 0:
            raise forms.ValidationError('This animal has been created already.')
        return self.cleaned_data['name']
    def clean_image(self):
        return self.cleaned_data['image']
    class Meta:
        model = Animal
        fields = ['name', 'description', 'image']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','cols':50}),
            'image':forms.FileInput(attrs={'class':'form-control-file'})
        }

class Add_post_form(forms.ModelForm):
    def clean_text(self):
        if len(self.cleaned_data['text']) < 10:
            raise forms.ValidationError('Your post is too small. Try to find more info.')
        return self.cleaned_data['text']
    class Meta:
        model = Post
        fields = ['text',]
        widgets = {
            'text':forms.Textarea(attrs={'class':'form-control',
                                         'cols':20,
                                         'rows':5,
                                         })
        }
