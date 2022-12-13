from django import forms

# Create your tests here.

class Loginform(forms.Form):

    def __init__(self, *args, **kwargs):

        widget = forms.TextInput(attrs = {"class":"loginstyle"})
        pwdstyle = forms.PasswordInput(attrs = {"class":"loginstyle1"})

        super().__init__(*args, **kwargs)

        self.fields["Username"] = forms.CharField(widget=widget)
        self.fields["Password"] = forms.CharField(widget=pwdstyle)
        
    template_name_label = None

