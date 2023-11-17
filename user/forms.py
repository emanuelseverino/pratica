from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
