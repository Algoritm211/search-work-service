from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
        return redirect('home_page')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.save()
        messages.success(request, 'Пользователь был успешно добавлен в систему')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


    
def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные были успешно обновлены')
                return redirect('accounts:update')
    
        form = UserUpdateForm(initial={
            'city': user.city,
            'language': user.language,
            'send_email': user.send_email
        })
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            queryset = User.objects.get(pk=user.pk)
            queryset.delete()
            messages.error(request, 'Пользователь удален')
    return redirect('home_page')

