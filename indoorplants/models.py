from django.db import models
from myuser.models import MyUser

# planttype model is for database plants to pick from
class PlantType(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    common_name = models.CharField(max_length=50, blank=True, null=True,)
    photo = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None, blank=True, null=True,)
    SUNLIGHT = [
        ('Indirect', 'Indirect'),
        ('Direct', 'Direct'),
    ]
    sunlight_type = models.CharField(
        max_length=8,
        choices=SUNLIGHT,
        default=None,
        blank=True,
        null=True,
        )

    WATER = [
        ('check daily', 'check daily'),
        ('3-5 days', '3-5 days'),
        ('7-10 days', '7-10 days'),
        ('14-21 days', '14-21 days'),
        ('Monthly', 'Monthly'),
    ]
    water_freq = models.CharField(
        max_length=30,
        choices=WATER,
        default=None,
        blank=True,
        null=True,
        )

    SOILTYPE = [
        ('well draining', 'well draining'),
        ('moisture retaining', 'moisture retaining'),
    ]
    soil_type = models.CharField(
        max_length=50,
        choices=SOILTYPE,
        default=None,
        blank=True,
        null=True,
        )

    MOISTLEVEL = [
        ('Dry', 'Dry'),
        ('Damp', 'Damp'),
        ('Moist', 'Moist'),
        ('Wet', 'Wet'),
    ]
    moisture_level = models.CharField(
        max_length=5,
        choices=MOISTLEVEL,
        default=None,
        blank=True,
        null=True,
        )

    common_problems = models.CharField(max_length=150, blank=True, null=True)
    notes = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        if self.common_name:
            return f'{self.name} ({self.common_name})'
        else:
            return self.name


# plant model is each instance of a planttype plant for individual user instance
class Plant(models.Model):
    planttype = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    watering = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.planttype.name

