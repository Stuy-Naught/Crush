from django import forms
import re
from crush_connector.models import Crush

class RegisterForm(forms.Form):
    name = forms.CharField(label=u'Name', error_messages = {'required':''})
    email = forms.EmailField(label=u'Email', error_messages = {'required':''})

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for i in range(Crush.num_allowed_crushes):
            self.fields['Crush_email_%d' % (i+1)] = forms.EmailField(required=(i==0))
            # require at least one crush email, but not the others