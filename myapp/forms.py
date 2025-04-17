from django import forms
from .models import user_register
from captcha.fields import CaptchaField


class user_registerForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    captcha = CaptchaField()

    class Meta:
        model = user_register
        fields = ['profile_picture', 'full_name', 'username', 'email', 'password', 'confirm_password', 'gender', 'age', 'captcha']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import user_register

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = user_register
        fields = [
            'profile_picture',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'gender',
            'age',
            'nationality',
            'city',
            'postal_address',
            'mobile_no',
            'preferred_travel_season',
            'preferred_travel_type',
            'age_range',
            'budget_range',
            'last_visited_destination'
        ]



from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'review_image']

from django import forms
from .models import Like, Reply

# Form for the Like model (no fields needed, because we only need user and review)
class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []  # No fields required, we use the review_id and user from session

# Form for the Reply model
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['comment']  # Only need the comment for a reply


from django import forms
from .models import TravelPlan

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = ['title', 'destinations', 'start_date', 'end_date', 'budget', 'notes', 'status']

        widgets = {
            'start_date': forms.SelectDateWidget(),
            'end_date': forms.SelectDateWidget(),
        }


from django import forms
from .models import Booking, TravelPlan

class BookingForm(forms.ModelForm):
    # Specify that start_date and end_date are date fields
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)  # Optional field

    class Meta:
        model = Booking
        fields = ['booking_type', 'provider_name', 'booking_reference', 'start_date', 'end_date', 'amount', 'status', 'notes', 'travel_plan']
