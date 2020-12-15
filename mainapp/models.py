from django.db import models

class Game(models.Model):
    game_name = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.pk) + ":"+ self.game_name

# Create your models here.
class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    photo_name = models.CharField(max_length=100, null=True, blank=True)
    position = models.IntegerField(default=0, null=False, blank=True)

    def __str__(self):
        return str(self.pk) + ":" +self.first_name + ' ' + self.last_name + " pos="+str(self.position)

class Gift(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE,default=None)
    original_owner = models.ForeignKey(Player, on_delete=models.CASCADE, null=False, blank=False, related_name='original_owner')
    current_owner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name='current_owner')
    file_name = models.CharField(max_length=100)
    locked = models.BooleanField(default=False, null=False, blank=False)
    number_of_times_stolen = models.IntegerField(default=0, null=False, blank=False)
    wrap = models.CharField(max_length=15, default=None, blank=True, null=True)
    def __str__(self):
        res = str(self.pk) + ":"+ self.file_name+" Current Owner="
        if self.current_owner is None:
            res = res + "None"
        else:
            res = res+self.current_owner.first_name
        return res

class GameProperties(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE,default=None)
    current_player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    next_position = models.IntegerField(default=0, null=False, blank=False) #this is next position on gift open
    no_lock_stage = models.BooleanField(default=False, null=False, blank=False)
    started = models.BooleanField(default=False, null=False, blank=False)
    ended = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return str(self.pk) + ":"+ self.game.game_name
