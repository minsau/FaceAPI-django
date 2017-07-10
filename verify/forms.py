from django import forms
 
class UploadForm(forms.Form):
  nombre_completo = forms.CharField(
    max_length=100,
    label="Nombre completo"
  )
  username = forms.CharField(max_length=20)
  docfile = forms.FileField(label='Selecciona un archivo')

class LoginForm(forms.Form):
  username = forms.CharField(
    max_length=100,
    label="Username"
  )
  docfile = forms.FileField(label='Selecciona un archivo')