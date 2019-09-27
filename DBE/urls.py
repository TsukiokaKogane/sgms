"""DBE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from default import views
urlpatterns = [
    path('', views.autoredirect),
    path('admin/', admin.site.urls),
    path('login/', views.loginview),
    path('login/submit', views.logindef),
    path('manage/', views.manageview),
    path('addstu/', views.newstuview),
    path('addstu/submit', views.newstudef),
    path('addtea/', views.newteaview),
    path('addtea/submit', views.newteadef),
    path('addcor/', views.newcorview),
    path('addcor/submit', views.newcordef),
    path('addcls/', views.newclsview),
    path('addcls/submit', views.newclsdef),
    path('delete/<int:ID>', views.deldef),
    path('deletec/<slug:course>/<int:ID>', views.delcdef),
    path('deletecl/<int:ID>', views.delcldef),
    path('edits/<int:ID>',views.editsview),
    path('edits/submit', views.editsdef),
    path('logout/', views.Logout),
    path('dashboard/',views.dashview),
    path('profile/', views.proview),
    path('gradelist/', views.graview),
    path('tprofile/', views.tproview),
    path('editg/submit', views.editgsub),
    path('editg/<int:cid>/<int:sid>', views.editgdef),
    path('chart/', views.chartview),
    path('resetp/submit', views.resetpdef),
    path('resetp/', views.resetpview),

    # path('profile/', views.testprofile),
    # path('dashboard/', views.testdashboard),
    # path('tprofile/', views.testtprofile),
    # path('gradelist/', views.testgardelist),
    # path('gradelist/editgrade/<int:ID>/<slug:course>', views.testeditgrade),
    # path('',views.testView)
    # path('test/',views.testView),
]
