from django import forms

from django.core import validators

from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    passwordValid = forms.CharField(max_length=100, 
                                    label = "Comfirm Password",
                                    widget=forms.PasswordInput)
    botcatcher = forms.CharField(required = False,                                  
                                 widget = forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
    
    class Meta:
        
        model = User
        fields = ("username", "first_name", "last_name", "email", "password",
                  "passwordValid")
    
    def clean_passwordValid(self):
            
            password = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("passwordValid")
            
            if password and password2 and password != password2:
                raise forms.ValidationError("Password don't match")
            return password
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already registered')
        return email
    
    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user