from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import CharField

class Page1Form(Form):
    error_css_class = 'error'
    id_num = CharField()
    
    
    def clean_id_num(self):
        if self.cleaned_data['id_num'] == 'error':
            raise ValidationError('Nespravne cislo')