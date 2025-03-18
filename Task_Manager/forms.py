from django import forms

from Task_Manager.models import *


# class UserForm(forms.Form):

#     username= forms.CharField(max_length=100)

#   === instead of this we can use ModelForm ===

class UserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ("username","first_name","last_name","email","password")

        widgets = {
                   'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your First Name'}),
                   'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Last Name'}),
                   'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}),
                   'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'})
                   }
        
        labels = {
                    "username": "User Name",
                    'last_name':'Last Name',
                    'first_name':'First Name'
                 }


class Loginform(forms.Form):


    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your UserName'}))

    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))


class Forgotform(forms.Form):

    user_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter UserName'}))

    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))

    new_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Passwoed'}))

    # labels = {
    #         'password':'New Password',
    #         }


class Taskform(forms.ModelForm):

    class Meta:

        model = TaskModel

        fields = ['Task_Name','Task_Description','Due_Date','Priority']

        widgets = {
                    'Task_Name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Task Name'}),
                    'Task_Description':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Task Description'}),
                    'Due_Date':forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Enter Due date','type':'date'}),
                    'Priority':forms.Select(attrs={'class':'form-control'})
                  }