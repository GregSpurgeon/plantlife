from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.views.generic import View

from indoorplants.models import Plant, PlantType
from journal.models import Entry
from myuser.models import MyUser
from plantcalendar.models import PlantWateringEntry

from indoorplants.forms import AddPlantTypeForm


class PlantView(View):
    def get(self, request, plant_id):
        plant = Plant.objects.get(id=plant_id)
        journal = Entry.objects.filter(plant=plant_id).order_by("created")[::-1]
        nickname = request.GET.get('nickname')
        watering = request.GET.get('watering')
        if nickname: 
            plant.nickname = nickname
            plant.save()
        if watering:
            plant.watering = watering
            plant.save()

            all_watering_entries = PlantWateringEntry.objects.filter(plant=plant)
            for entry in all_watering_entries:
                entry.delete()

            date = datetime.today()
            days = int(watering)
            next_date = date + timedelta(days=days)
            notes = "Time to water"
            rec_date = next_date           
            for _ in range(150):
                PlantWateringEntry.objects.create(
                    owner=plant.owner,
                    plant=plant,
                    notes=notes,
                    entry_date=rec_date,
                )
                rec_date += timedelta(days=days)
        return render(request, 'plantdetail.html', {'plant': plant, 'journal': journal})


class LibraryView(View):
    def get(self, request):
        library = PlantType.objects.filter(Q(author=1) | Q(author=request.user.id))
        return render(request, 'plantlibrary.html', {'library': library})


class PlantTypeView(View):
    def get(self, request, plant_id):
        plant_type = PlantType.objects.get(id=plant_id)
        return render(request, 'p_library_details.html', {'plant': plant_type})


@login_required
def alt_watering(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    all_watering_entries = PlantWateringEntry.objects.filter(plant=plant)
    for entry in all_watering_entries:
        entry.delete()

    date = datetime.today()
    days = plant.watering
    next_date = date + timedelta(days=days)
    notes = "Time to water"
    rec_date = next_date           
    for _ in range(100):
        PlantWateringEntry.objects.create(
            owner=plant.owner,
            plant=plant,
            notes=notes,
            entry_date=rec_date,
        )
        rec_date += timedelta(days=days)

    return HttpResponseRedirect(reverse('plant', kwargs={'plant_id': plant.id}))


@login_required
def add_plant(request, plant_id):
    me = request.user
    parent_plant = PlantType.objects.get(id=plant_id)
    # create an instance of a parent plant with added fields
    new_plant = Plant.objects.create(
        planttype=parent_plant,
        owner=request.user
    )
    text = f"""A new plant was added to your profile. You can set a custom
        watering schedule/reminder based on your plants actual needs. Don't forget
        to give it a nickname. You can also add your own photos to your journal posts to 
        help you monitor any changes in your plant.... Happy Tracking!!"""
    Entry.objects.create(
        author=me,
        text=text,
        plant=new_plant
    )
    return HttpResponseRedirect(reverse('plant', kwargs={'plant_id': new_plant.id}))


class AddPlantType(View):
    form_class = AddPlantTypeForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'generic_form.html', {'form': form, 'errors': None})
    
    def post(self, request):    
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                PlantType.objects.create(
                    name=data['name'],
                    author=MyUser.objects.get(username=request.user.username),
                    common_name=data['common_name'],
                    photo=data['photo'],
                    sunlight_type=data['sunlight_type'],
                    water_freq=data['water_freq'],
                    soil_type=data['soil_type'],
                    moisture_level=data['moisture_level'],
                    common_problems=data['common_problems'],
                    notes=data['notes']
                )
                return HttpResponseRedirect(request.GET.get('next', reverse('library')))


@login_required
def remove_plant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return HttpResponseRedirect(reverse('homepage'))
