from django.shortcuts import render

def home(request):
    print("DEBUG: home view reached!") # Debug print
    return render(request, 'home.html')
