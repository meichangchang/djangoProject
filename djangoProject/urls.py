"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from .views import hello
from djangoProject.views import hello_button
from djangoProject.views import hello_button_one
from djangoProject.views import hello_button_result
from djangoProject.views import hello_button_test
from djangoProject.views import hello_button_testResult
from djangoProject.views import hello_button_testResult2
from djangoProject.views import hello_button_search
from djangoProject.views import hello_button_searchResult
from djangoProject.views import hello_bikeng
from djangoProject.views import hello_button_predict_one
from djangoProject.views import hello_button_predict_two
from djangoProject import views
from django.conf.urls import url

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^ni/$', views.index),
    url(r'^regist/$', views.regist),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    path('', hello_button),
    path('yusuan/', hello_button_one),
    path('bikeng/', hello_bikeng),
    path('yuce/', hello_button_predict_one),
    path('yuce/predict_result_two.html', hello_button_predict_two),
    path('yusuan/result.html', hello_button_result),
    path('yusuan/styleTest.html', hello_button_test),
    path('yusuan/styleTestResult.html', hello_button_testResult),
    path('yusuan/styleTestResult2.html', hello_button_testResult2),
    path('yusuan/search.html', hello_button_search),
    path('yusuan/searchResult.html', hello_button_searchResult),
    path('history/', views.history),
]
