from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class TeamManager(models.Manager):
    def create_team(self, name, **kwargs):
        team = self.model()
        team.name = name

        team.save(using = self._db)
        return team

    def get_all_team(self):
        return Team.objects.all()

class Team(models.Model):
    """
    team model functions
    - team_name
    - team_contact_number
    - team_website_url
    
    """
    objects = TeamManager()
    name = models.CharField(max_length = 30)
    contact_number = models.CharField(max_length = 20)
    website_url = models.URLField(max_length = 50)
    users = models.ManyToManyField(User, through = 'Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    date_joined = models.DateField()
    is_admin = models.BooleanField(default=False)
