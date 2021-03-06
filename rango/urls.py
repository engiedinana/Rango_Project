from django.urls import path
from rango import views
app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category,name='show_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'), 
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # facebook related URLs
    path('facebook_login/', views.facebook_login, name="facebook_login"),
    path('facebook_register/', views.facebook_register, name="facebook_register"),

    # terms of use page URL
    path('terms_of_use/', views.terms_of_use, name="terms_of_use"),
    # Get DB categories to display in homepage URL
    path('get_cat/', views.get_cat, name="get_cat"),
    # added the username to the category to know who created it for future improvements
    path('add_category/<username>/', views.add_category, name='add_category'),
    # Rating for categories URL
    path('rate_category/<slug:category_name_slug>/<star>', views.rate_category, name="rate_category"),

    #route for saving a favorite page and view to fire
    path('save_favorite/',views.SaveFavoriteView.as_view(), name="save_favorite"),
    #route for unsaving a favorite page and corresponding view to fire
    path('unsave_favorite/', views.UnsaveFavoriteView.as_view(), name="unsave_favorite"),
    #route to display a user's profile and corresponding view to fire
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    #route for contactus page
    path('contactus/', views.ContactUsView.as_view(), name="contact_us"),
]