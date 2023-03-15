"""Django forms module."""
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]

    first_name = CharField(label=_('Name'), required=True)

    last_name = CharField(label=_('Surname'), required=True)

    username = CharField(
        label=_('Username'),
        help_text=_("Required field. 150 symbols max. "
                    "It can contain only letters,"
                    " digits and symbols @/./+/-/_."),
        required=True,
    )

    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput,
        help_text=_('<ul><li>Your password must contain'
                    ' at least 3 symbols.</li></ul>'),
    )

    password2 = CharField(
        label=_("Password confirm"),
        widget=PasswordInput,
        help_text=_('Please, enter password again for confirmation.')
    )

    def clean_password2(self):
        """Password validation"""
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 != pass2:
            raise ValidationError(_("Passwords do not match"))
        if len(pass2) < 3:
            raise ValidationError(_("Password is too short."
                                    " It must contain at least 3 symbols."))
        return pass2

    def save(self, commit=True):
        """Saving password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
