# accounts/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import UsersSerializer

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('registerUsername')
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')
        print(username, email, password)
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return JsonResponse({'message': 'Registration successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def send_test_reset_email(request):
    user = User.objects.get(username='testuser')  # Replace 'testuser' with the user's username or email
    token = default_token_generator.make_token(user)
    domain = request.get_host()
    url = reverse('password_reset_confirm', args=[user.pk, token])
    reset_link = f"http://{domain}{url}"
    send_mail(
        'Password Reset',
        f'Click the following link to reset your password: {reset_link}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
    return HttpResponse('Test email sent.')
    

@api_view(['POST'])
def add_users(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    return Response(serializer.errors, status=400)