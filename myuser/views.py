from datetime import datetime
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from authentication.forms import SignUpForm
from myuser.models import MyUser
from indoorplants.models import Plant, PlantType
from indoorplants.bootstrap_data import generate_data_planttype
from plantcalendar.models import PlantCalendarEntry, PlantWateringEntry
from journal.models import Entry
# Create your views here.

def index_view(request):
    if not PlantType.objects.all():
        generate_data_planttype()
    if request.user.is_authenticated:
        my_user = MyUser.objects.filter(username=request.user.username).first()
        plants = Plant.objects.filter(owner=request.user)
        today = datetime.today()
        cal_entries = PlantCalendarEntry.objects.filter(owner=my_user)
        entry_list = cal_entries.filter(entry_date=today)
        w_entries = PlantWateringEntry.objects.filter(owner=my_user)
        w_entry_list = w_entries.filter(entry_date=today)
    else:
        my_user = MyUser.objects.filter(username='admin').first()
        plants = ''
        entry_list = None
        w_entry_list = None
    return render(request, 'index.html', {'my_user': my_user, 'plants': plants, 'list_for_today': entry_list, 'w_entry_list': w_entry_list})


@login_required()
def profile(request, username):
    my_user = MyUser.objects.filter(username=username).first()
    return render(request, 'profile.html', {'my_user': my_user})


@login_required()
def edit_profile(request, username):
    me = MyUser.objects.filter(username=username).first()
    if request.method == "POST":
        form = SignUpForm(request.POST, instance=me)
        if form.is_valid():
            data = form.cleaned_data
            me.username = data['username']
            me.set_password(data['password'])
            me.email = data['email']
            me.first_name = data['first_name']
            me.last_name = data['last_name']
            me.save()
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

    form = SignUpForm(instance=me)
    return render(request, "generic_form.html", {'form': form, 'my_user': me})

@login_required()
def delete_profile(request, user_id):
    user = MyUser.objects.get(id=request.user.id)
    user.delete()
    return HttpResponseRedirect(reverse('homepage'))
