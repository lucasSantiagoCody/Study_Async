from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    class Meta:
        add = CustomUserCreationForm
        form = CustomUserChangeForm
        model = User 
        list_display = ('email', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)