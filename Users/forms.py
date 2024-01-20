from django.forms import Form 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ('email', 'password',)
    
class CustomUserChangeForm(UserChangeForm):
    class Meta: 
        model = User 
        fields = ('email', 'password',)