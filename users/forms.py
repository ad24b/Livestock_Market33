from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import SellerRequest

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

# ✨ نموذج تعديل الملف الشخصي (لرفع صورة الملف والغلاف)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'cover_image']




class SellerRequestForm(forms.ModelForm):
    class Meta:
        model = SellerRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'أخبرنا لماذا تريد أن تصبح بائعًا...'}),
        }

