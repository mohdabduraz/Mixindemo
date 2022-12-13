# Mixindemo

In the forms.py I think you can optimize it a bit like

```python
from django import forms

class Loginform(forms.Form):
    # Define the widgets as class attributes
    widget = forms.TextInput(attrs = {"class":"loginstyle"})
    pwstyle = forms.PasswordInput(attrs = {"class":"loginstyle1"})

    # Use the widgets in the field definitions
    Username = forms.CharField(widget=widget)
    Password = forms.CharField(widget=pwstyle)
```

```python
from django import forms

class Loginform(forms.Form):
    def __init__(self, *args, **kwargs):
        # Define the widgets in the __init__ method
        widget = forms.TextInput(attrs = {"class":"loginstyle"})
        pwstyle = forms.PasswordInput(attrs = {"class":"loginstyle1"})

        super().__init__(*args, **kwargs)

        # Use the widgets in the field definitions
        self.fields['Username'] = forms.CharField(widget=widget)
        self.fields['Password'] = forms.CharField(widget=pwstyle)
```
