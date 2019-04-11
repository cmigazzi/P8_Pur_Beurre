from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
                max_length=254, label='E-mail',
                widget=forms.TextInput(attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Votre adresse e-mail..."}))
    password = forms.CharField(
                label='Mot de passe',
                widget=forms.PasswordInput(attrs={
                    "class": "form-control",
                    "placeholder": "Mot de passe"}))


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(
                max_length=254, label='E-mail',
                widget=forms.TextInput(attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Votre adresse e-mail..."}))
    password1 = forms.CharField(label='Mot de passe',
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control mb-2",
                                    "placeholder": "Mot de passe..."}
                                ))
    password2 = forms.CharField(label='Confirmer le mot de passe',
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control",
                                    "placeholder": "Confirmer le mot de passe."}
                                ))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
