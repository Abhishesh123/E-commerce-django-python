from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
import random
from django.contrib import messages
from core.models import Customer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required


# Amulya
def user_register(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            gender = request.POST.get('gender')
            phone_number = request.POST['phone_number']

            if password1 == password2:
                if Customer.objects.filter(email=email).exists():
                    return render(request, 'accounts/register.html', context={'message': "Email already exists."})
                else:
                    username = first_name.replace(' ', '_').lower() + last_name.lower() + str(random.randint(1, 100))
                    while Customer.objects.filter(username=username).exists():
                        username = first_name.replace(' ', '_').lower() + last_name + str(random.randint(1, 100))
                    user = Customer.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                        email=email, password=password1,
                                                        gender=gender, phone_number=phone_number)
                    user.save()

                    html_content = render_to_string('accounts/email_confirmation.html')

                    text_content = strip_tags(html_content)

                    msg = EmailMultiAlternatives('You are now registered', text_content,
                                                 'contact.realestate.information@gmail.com', [email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    messages.success(request, "You have been successfully registered. Login now!")
                    return redirect('accounts:login_app')
            else:
                return render(request, 'accounts/register.html', context={'message': "Passwords do not match"})
        return render(request, 'accounts/register.html')
    else:
        return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


#Aman
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            current_customer = Customer.objects.get(email=email)
            user_authenticated = authenticate(request, username=current_customer.username, password=password)
            if user_authenticated is not None:
                login(request, user_authenticated)
                return redirect('index')
            else:
                context = {'message': 'Incorrect Password'}
        except Customer.DoesNotExist:
                context = {'message': 'No such user exist'}
        return render(request, 'accounts/login.html', context=context)
    else:
        if not request.user.is_authenticated:
            return render(request, 'accounts/login.html')
        else:
            return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('accounts:login_app')


#Aayush
def check_email(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        user_email = Customer.objects.filter(email=mail)
        if user_email:
            request.session['user_email'] = mail
            return redirect('password_reset')
        else:
            messages.error(request, "Not a registered email")
            return redirect('check_email')
    else:
        return render(request, 'accounts/check_mail.html')


@login_required(login_url='/account/login')
def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = Customer.objects.get(username__exact=request.user.username)

        if password1==password2:
            if user.check_password(request.POST['old_password']):
                user.set_password(password1)
                user.save()
                return redirect('password_reset_complete')
            else:
                messages.error(request, "The old password you have entered is wrong")
                return render(request, 'accounts/reset_password.html')

        else:
            messages.error(request, "Password does not match")
            return render(request, 'accounts/reset_password.html')

    else:
        return render(request, 'accounts/reset_password.html')




#Deepak