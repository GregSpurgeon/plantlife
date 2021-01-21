from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from authentication.views import LoginView, LogoutView, SignUpView, about
from plantcalendar.views import CalendarView, CreateCalEntry, remove_calendar_entry
from journal.views import CreateEntryView, remove_entry
from myuser.views import index_view, profile, edit_profile, delete_profile
from indoorplants.views import PlantView, AddPlantType, PlantTypeView, LibraryView
from indoorplants.views import add_plant, remove_plant, alt_watering


urlpatterns = [
    path('', index_view, name="homepage"),
    path('about/', about, name="about"),
    path('accounts/<str:username>/', profile, name='profile'),
    path('add_plant/<int:plant_id>/', add_plant, name='add_plant'),
    path('add_plant_type/', AddPlantType.as_view(), name="add_plant_type"),
    path('admin_site/', admin.site.urls),
    path('all_plants/', LibraryView.as_view(), name='library'),
    path('alt_watering/<int:plant_id>/', alt_watering, name='alt_watering'),
    path('calendar/', CalendarView.as_view(), name="calendar"),
    path('calendar/entry', CreateCalEntry.as_view(), name="calendar_entry"),
    path('calendar/edit/<int:entry_id>/', CreateCalEntry.as_view(), name="edit_entry"),
    path('delete_profile/<int:user_id>/', delete_profile, name='delete_profile'),
    path('edit/<str:username>/', edit_profile, name='edit_profile'),
    path('journal_entry/<int:plant_id>/', CreateEntryView.as_view(), name='new_entry'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('plant/<int:plant_id>/', PlantView.as_view(), name='plant'),
    path('plant_type/<int:plant_id>/', PlantTypeView.as_view(), name='plant_type'),
    path('remove_calendar_entry/<int:entry_id>/', remove_calendar_entry, name='remove_calendar_entry'),
    path('remove_entry/<int:entry_id>/', remove_entry, name='remove_entry'),
    path('remove_plant/<int:plant_id>/', remove_plant, name='remove_plant'),
    path('sign_up/', SignUpView.as_view(), name='sign_up')

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'authentication.views.page_not_found'
handler500 = 'authentication.views.internal_server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
