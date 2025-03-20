from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View
from django.contrib.auth import authenticate,login,logout

from Task_Manager.forms import *
from Task_Manager.models import *

from django.contrib import messages
from django.contrib.auth.hashers import make_password

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json


def is_user(fn):   # creating a decorator to check the operation is done by the logged in user & the taskmodel id is created by user logged in

    def wrapper(request,**kwargs):

        data = TaskModel.objects.get(id = kwargs.get('pk'))
        if data.user == request.user:
            return fn(request,**kwargs)
        
        else:
            return redirect('login')

    return wrapper


def is_login(fn):

    def wrapper(request):

        if not request.user.is_authenticated:
            return redirect('login')
        
        else:
            return fn(request)
        
    return wrapper


def loggedin(fn):
    def wrapper(request):      
        if request.user.is_authenticated:
            return redirect('userpage')
        else:
            return fn(request)
    return wrapper




# Create your views here.
# view : UserRegistration 
# method : get , post
# url : localhost - 127.0.0.1:8000/Task_manager/signup


class Home_View(View):

    def get(self,request):

        return render(request,'index.html')


@method_decorator(decorator=is_login,name='dispatch')
class Userpage_View(View):

    def get(self,request):

        tasks = TaskModel.objects.filter(user=request.user).order_by('Status')
        data = TaskModel.objects.filter(user = request.user)
        today = timezone.localdate()

        sum = 0
        for i in data:
            sum += i.Points

        return render(request,'user_page.html',{'tasks':tasks,'sum':sum,'today':today})
    


class Logout_View(View):

    def get(self,request):

        logout(request)

        return redirect('login')



class User_SignUp_View(View):

    def get(self,request):

        form = UserForm

        return render(request,'registration.html',{'new':form})
    
    def post(self,request):

        form = UserForm(request.POST)

        if form.is_valid():

            # print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            
            messages.success(request,"User Registration Sucessfull, Please LogIn")
        
            return redirect('home')

        else:

            return redirect('signup') 


@method_decorator(decorator=loggedin,name='dispatch')
class User_login_view(View):

    def get(self,request):

        form = Loginform()

        return render(request,'login.html',{'new':form})
    # @loggedin
    def post(self,request):

        form = Loginform(request.POST)

        if form.is_valid():

            u_name = request.POST.get('username')
            pwd = request.POST.get('password')

            user_obj = authenticate(request,username=u_name,password=pwd)   # here username=u_name is called keyword argument , not default arguent

            if user_obj:

                login(request,user_obj)
                return redirect('userpage')

            else:

                messages.error(request,"Invalid Username and Password")

        form = Loginform
        return render(request,'login.html',{'new':form})
        


class Forgot_View(View):

    def get(self,request):

        form = Forgotform()

        return render(request,'forgot.html',{'forgot':form})
    
    def post(self,request):

        form = Forgotform(request.POST)

        if form.is_valid():

            user_id = form.cleaned_data['user_id']
            email_address = form.cleaned_data['email_address']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(username=user_id,email=email_address)
                user.password = make_password(new_password)
                user.save()

                return render(request,'pass_ch_sucessfull.html')


            except User.DoesNotExist:

                messages.error(request, "No matching user found. Please check your details.")

        return render(request,'forgot.html',{'forgot':form})



@method_decorator(decorator=is_login,name='dispatch')
class TaskAdd_view(View):

    def get(self,request):

        form = Taskform

        return render(request,'taskadd.html',{'form':form})
    
    def post(self,request):

        form = Taskform(request.POST)

        if form.is_valid():

            TaskModel.objects.create(**form.cleaned_data,user = request.user)   # this user(request.user) not represent the table User, this is another django keyword to get which user is loggedin , ie his id

        messages.success(request,'Task Added succesfully')
        return redirect('userpage')
    


# class TaskDeleteView(View):     # This view is to delete the task using url , by inputing the id of the task to be deleted in the url itself
#                                 # This view delete a tsk in TaskModel , it doesnot need a user login , just deleteing an object from TaskModel
#     def get(self,request,**kwargs):  # kwargs is a dict which will hold the id which was inputed in the url ('pk':id(eg : 2)) - 'pk' --> key

#         c_id = kwargs.get('pk')

#         data = TaskModel.objects.get(id = c_id)

#         data.delete()   # all of this can be written in one code --> TaskModel.objects.get(id = kwargs.get('pk')).delete()

#         return redirect('userpage')


@ method_decorator(decorator=is_user,name="dispatch")  # here decorator is callled , it checked if logged user is the one who tries to delete the task_id,
                                                       # if not , it will redirect to 'login'- else if user : task will be deleted
class TaskDeleteView(View):

    def get(self,request,**kwargs):

        data = TaskModel.objects.get(id = kwargs.get('pk'))

        # if data.user == request.user:

        data.delete()
        return redirect('userpage')
        
        # else:

        #     return redirect('login')



class TaskUpdate_view(View):

    def get(self,request,**kwargs):

        data = get_object_or_404(TaskModel,id=kwargs.get('pk'),user=request.user)

        form = Taskform(instance = data)  # we can only use instance in modelform

        return render(request,'update.html',{'form':form})

    def post(self,request,**kwargs):

        data = get_object_or_404(TaskModel,id=kwargs.get('pk'),user=request.user)  # ensures task belong to user if not reurns a 404 page innstead of error
        form = Taskform(request.POST,instance=data)

        if form.is_valid():

            data.Status=False
            form.save()
            messages.success(request,"Task Updated successfully")
            return redirect('userpage')
        
        messages.error(request,"Error updating task. Please check your input")
        return render(request,'update.html',{'form':form})



@ method_decorator(decorator=is_user,name="dispatch")       # calling the decorator
class TaskSelectView(View):

    def get(self,request,**kwargs):

        data = TaskModel.objects.filter(id = kwargs.get("pk"))

        return render(request,'task_see.html',{'data':data})
    


class Task_complete_view(View):

    def get(self,request,**kwargs):

        data = TaskModel.objects.get(id = kwargs.get('pk'))

        # if data.Status == False:

        data.complete()     # this method contain the if and save conditions, so no need to add more (for updating points)

            # data.save()

        return redirect('userpage')



class Task_progress_view(View):             # Do it as a JS Chart

    def get(self,request):

        total = TaskModel.objects.filter(user = request.user).count()

        completed = TaskModel.objects.filter(user = request.user , Status = True).count()

        incomplete = TaskModel.objects.filter(user = request.user , Status = False).count()

        chart_data = json.dumps([completed, incomplete, total])

        return render(request,'task_progress.html', {'chart_data': chart_data})