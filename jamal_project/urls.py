"""
URL configuration for jamal_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
urlpatterns = [
path('admin/', admin.site.urls),
path('', include('home.urls')),
path('construction/', include('construction.urls')),
path('finance/', include('finance.urls')),

path('project/', include('project.urls')),

path('account/', include('account.urls')),  
path('accounts/', include('accounts.urls')),      

path('salesmarketing/', include('salesmarketing.urls')),   
path('customerdetailed/', include('customerdetailed.urls')),  
path('lead/', include('lead.urls')), 
path('contractor/', include('contractor.urls')),

path('customerbill/', include('customerbill.urls')),
path('chloridetest/', include('chloridetest.urls')),

path('proposals/', include('proposals.urls')),
path('requisition/', include('requisition.urls')),
path('contractorbill/', include('contractorbill.urls')),
path('resource/', include('resource.urls')),
path('pr/', include('pr.urls')),


]
