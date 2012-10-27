from django import forms
import re
from crush_connector.models import Crush

class RegisterForm(forms.Form):
    name = forms.CharField(label=u'', error_messages = {'required':''})
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for i in range(Crush.num_allowed_crushes):
            self.fields['email_%d' % i] = forms.EmailField()
