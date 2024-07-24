from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'Training/layout.html')
def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        