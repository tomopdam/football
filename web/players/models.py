from django.db import models

class Player(models.Model):
    id_ext = models.IntegerField()
    name = models.CharField(max_length=50)
    age = models.SmallIntegerField()
    photo = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    overall = models.SmallIntegerField()
    value = models.IntegerField()
    wage = models.IntegerField()
    position = models.CharField(max_length=3)
    release_clause = models.IntegerField()
    group = models.CharField(max_length=2)
    photo_exists = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'players'
