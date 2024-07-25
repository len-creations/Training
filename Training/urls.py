from django.urls import path
from django.conf.urls import handler404
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view, name="login"),
    path("Register",views.register,name="register"),
    path("logout",views.logout_view, name="logout"),
    path('create_profile/', views.update_profile, name='update_profile'),
    path("success",views.success_page, name="success_page"),
    path("Profile_pic",views.Profile_pic,name='Profile_pic')

]
#custom handler for 404 errors
handler404 = 'Training.views.custom_404_view'