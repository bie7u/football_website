from django.urls import path
from .import views
from allauth.account.views import LoginView, SignupView, ConfirmEmailView


urlpatterns = [
    path('logowanie/', LoginView.as_view(), name="custom_login" ),
    path('rejestracja/', SignupView.as_view(), name="custom_register"),
    path('rejestracja/potwierdź_email/', ConfirmEmailView.as_view(), name="confirm_email_custom"),
    path('menu_użytkownika/zobacz_profil/', views.editProfile, name='edit-profile'),

    # HTMX
    path('zmien_haslo/', views.changePassword, name='change-password-user')
]