from django import forms
from django.forms.widgets import PasswordInput
from django.utils.timezone import datetime
from .models import Blog,User

ADVANCE_RESERVATION_DAYS = 14


class RegisterForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    reg_login = forms.CharField(label="Login", max_length=20)
    reg_password = forms.CharField(
        label="Password", max_length=20, widget=forms.PasswordInput()
    )
    passagain = forms.CharField(
        label="Password again", max_length=20, widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reg_login"].widget.attrs["hx-post"] = "/do_check_regform"
        self.fields["reg_password"].widget.attrs["hx-post"] = "/do_check_regform"
        self.fields["passagain"].widget.attrs["hx-post"] = "/do_check_regform"
        self.fields["reg_login"].widget.attrs["hx-target"] = "#check_regform_result"
        self.fields["reg_password"].widget.attrs["hx-target"] = "#check_regform_result"
        self.fields["passagain"].widget.attrs["hx-target"] = "#check_regform_result"


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=20)
    password = forms.CharField(label="Password", max_length=20, widget=PasswordInput())


class DateInput(forms.DateInput):
    input_type = "date"

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'photos']

class AuthorSelectForm(forms.Form):
    author = forms.ChoiceField(label="Select Author", choices=[])

    def __init__(self, *args, **kwargs):
        authors = kwargs.pop("authors")
        super(AuthorSelectForm, self).__init__(*args, **kwargs)

        # 著者の選択肢を設定
        self.fields["author"].choices = zip(authors, authors)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'icon', 'profile']
        widgets = {
            'password': forms.PasswordInput(),
        }

# class AuthorSelectForm(forms.Form):
#     author = forms.ChoiceField(label='Author', required=False)
#     date = forms.DateField(label='Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

#     def __init__(self, *args, **kwargs):
#         authors = kwargs.pop('authors', [])
#         super().__init__(*args, **kwargs)
#         self.fields['author'].choices = [('','All Authors')] + [(author.name, author.name) for author in authors]

class AuthorSelectForm(forms.Form):
    author = forms.ChoiceField(label='Author', required=False)
    date = forms.DateField(label='Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    keyword = forms.CharField(label='Keyword', required=False)

    def __init__(self, *args, **kwargs):
        authors = kwargs.pop('authors', [])
        super().__init__(*args, **kwargs)
        self.fields['author'].choices = [('','All Authors')] + [(author.name, author.name) for author in authors]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'icon', 'profile']
        labels = {
            'name': 'Display Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
            'profile': forms.Textarea(attrs={'class': 'form-control'}),
        }