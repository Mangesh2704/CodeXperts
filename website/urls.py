from django.urls import path
from django.conf import settings
from .views import home, about, service, pricing, blog, blog_details, contact, catalogue, store, genstores, get_districts, get_stores, search_medicines, login_view, signup_view, profile_view, newhome, awareness, newcontact
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('service', service, name='service'),
    path('pricing', pricing, name='pricing'),
    path('blog', blog, name='blog'),
    path('blogdetails', blog_details, name='blog_details'),
    path('contact', contact, name='contact'),
    path('catalogue/', catalogue, name='catalogue'),
    path('store', store, name='store'),
    path('genstores', genstores, name='genstores'),
    path('get-districts/', get_districts, name='get_districts'),
    path('get-stores/', get_stores, name='get_stores'),
    path('catalogue-list/', search_medicines, name='catalogue-list'),
    path('login/', login_view, name='login'),  # updated to login_view
    path('signup/', signup_view, name='signup'),  # added signup path
    # path('verify-otp/', verify_otp, name='verify_otp'),
    path('profile/', profile_view, name='profile'),
    
    # After Login
    path('', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', newhome, name='newhome'),
    path('awareness/', awareness, name='awareness'),
    path('contact/', newcontact, name='newcontact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
