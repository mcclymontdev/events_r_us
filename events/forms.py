from django_registration.forms import RegistrationForm

from events.models import User

class signUpForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
            "picture",
            "location",
        ]