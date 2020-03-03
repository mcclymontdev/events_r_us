from django_registration.forms import UserCreationForm
from django_registration import validators

from events.models import User

class signUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            "password1",
            "password2",
        ]

    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "reserved_names"):
            reserved_names = self.reserved_names
        else:
            reserved_names = validators.DEFAULT_RESERVED_NAMES
        username_validators = [
            validators.ReservedNameValidator(reserved_names),
            validators.validate_confusables,
        ]
        self.fields[User.USERNAME_FIELD].validators.extend(username_validators)