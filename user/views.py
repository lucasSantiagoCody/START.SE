from .fields_validators import email_validator, password_validator, username_validator
from django.contrib.auth import get_user_model
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse


def signup_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmation_password = request.POST.get('confirmation_password')
        

        if password == confirmation_password:
            single_message = ''

            check_username = username_validator(username)
            check_email = email_validator(email)
            check_passoword = password_validator(password)

            if not check_username:
                single_message += 'Username deve ter mais de 3 caracteres'
            if not check_email:
                # I don't recommend this message format be more specific
                single_message += ', Email inválido ou já esta sendo usado'
            if not check_passoword:
                single_message += ', Senha deve ter mais de 6 caracteres'    

            if single_message == '':
                try:
                    user = get_user_model().objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    if user:
                        messages.add_message(request, constants.SUCCESS, 'Registrado com sucesso')
                        return redirect(reverse('login_url'))
                except:
                    messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            else:
                messages.add_message(request, constants.WARNING, single_message)
        else:
            messages.add_message(request, constants.WARNING, 'Senhas não coicidem')

        return redirect(reverse('signup_url'))
      