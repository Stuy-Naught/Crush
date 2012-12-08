from django import forms
import re
from crush_connector.models import Crush



class RegisterForm(forms.Form):
    error_css_class = "control-group error"
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for i in range(Crush.num_allowed_crushes):
            self.fields['Crush_email_%d' % (i+1)] = forms.EmailField(required=(i==0))
            # require at least one crush email, but not the others

    def validate(self, value):
        "Check if value consists only of valid MIT emails."
        super(MultiEmailField, self).validate(value)
        try:
            Person.objects.get(email=value)
        except:
            raise ValidationError()
