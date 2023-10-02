from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import IrisData
import pandas as pd
from io import StringIO
import asyncio
from channels.db import database_sync_to_async
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync

@database_sync_to_async
def bulk_upload(df):
    iris_data_objects = [
        IrisData(
            sepal_length=row['SepalLengthCm'],
            sepal_width=row['SepalWidthCm'],
            petal_length=row['PetalLengthCm'],
            petal_width=row['PetalWidthCm'],
            species=row['Species']
        )
        for _, row in df.iterrows()
    ]

    # Use bulk_create to insert all objects in a single query
    IrisData.objects.bulk_create(iris_data_objects)

async def async_bulk_upload(df):
    await bulk_upload(df)

@sync_to_async
@login_required(login_url='/login')
@async_to_sync
async def handle_upload(request):
    if request.method == 'POST':
        fm = UploadForm(request.POST, request.FILES)
        if fm.is_valid():
            csv_file = fm.cleaned_data['file']
            
            # Decode the bytes into a string and then read into a DataFrame
            csv_content = csv_file.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            
            # Perform bulk upload asynchronously
            await async_bulk_upload(df)

            context = {'form': fm, 'list': await database_sync_to_async(list)(IrisData.objects.all())}
            return render(request, "index.html", context)  # Redirect to a success page

    fm = UploadForm()
    context = {'form': fm}
    return render(request, "index.html", context)



def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect("/register")
        
        user = authenticate(username = username,password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        else:
            login(request,user)
            return redirect("/handle-upload")
    
    return render(request , 'login.html')

def register(request):
    if request.method != "POST":
        return render(request , 'register.html')
    first_name=request.POST.get("first_name")
    last_name=request.POST.get("last_name")
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=User.objects.filter(username=username)
    if user.exists():
        messages.error(request, "This user already exists.")
        return redirect("register")
    user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
    )
    user.set_password(password)
    user.save()
    messages.info(request, "Account created Successfully")
    return redirect('register')

def logout_page(request):
    logout(request)
    return redirect('/login')