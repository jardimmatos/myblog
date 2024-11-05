from django import forms

class EmailForm(forms.Form):
    nome = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class':'form-control'}))
    comentario = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control','rows':'4'}),label="Comentário", )