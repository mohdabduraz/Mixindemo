from django import forms

# Create your tests here.

class Loginform(forms.Form):
    template_name_label = None
    widget = forms.TextInput(attrs = {"class":"loginstyle"})
    Username = forms.CharField(widget=widget)
    pwstyle = forms.PasswordInput()
    pwstyle.attrs["class"] = "loginstyle1"
    Password = forms.CharField(widget=pwstyle)
    
