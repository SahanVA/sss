"""ISP (SLIIT) URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from unicodedata import name
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="home"),
    path('login', views.home, name="login"),
    path('logins', views.logOp, name="logins"),
    path('signup', views.signup, name="signup"),
    path('saveAccount', views.saveAccount, name="saveAccount"),
    path('home', views.home, name="home"),
    path('analyse', views.analyse, name="analyse"),
    path('upload', views.uploadTwo, name="upload"),
    path('uploadPage', views.uploadPage, name="uploadPage"),
    path('download', views.downloadOnefile, name="download"),
    path('email', views.sendmail, name="email"),
    path('emails', views.sendmails, name="emails"),
    path('takePhotose', views.takePhoto, name="takePhotose"),
    path('update', views.saveEdt, name="update"),
    path('delete', views.deleteFile, name="delete"),
    path('personal', views.personal, name="personal"),
    path('disableAcc', views.accDisable, name="disableAcc"),
    path('personlup', views.persona, name="personlup"),
    path('upotp', views.uploadOtpPage, name="upotp"),
    path('upotpc', views.uploadOtpPageCom, name="upotpc"),
    path('format', views.processsFiles, name="format"),
    path('scn', views.clean_file_2, name="scn"),
    path('Critical', views.Critical, name="Critical")
]
