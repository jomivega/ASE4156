from django.shortcuts import render


def login(request):
    """
    Dummy function to render login page
    """
    return render(request, 'auth.html')
