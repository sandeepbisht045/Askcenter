from django.urls import path
from askcenter import views

urlpatterns = [
    path("signup",views.signup,name="signup"),
    path("login",views.user_login,name="login"),
    path("",views.askcenter,name="askcenter"),
    path("posts",views.user_posts,name="user_posts"),
    path("<int:q_id>/answers",views.user_answers,name="user_answers"),
    path("<int:a_id>/like",views.user_like,name="user_like"),
    path("logout",views.user_logout,name="logout"),
   
]