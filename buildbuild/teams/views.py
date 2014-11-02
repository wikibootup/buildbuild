from django.shortcuts import render
from django.http import HttpResponseRedirect,request
from django.http import HttpResponse

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import authenticate

from django.contrib import messages

from django.core.urlresolvers import reverse

from django.db import IntegrityError, OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from teams.forms import MakeTeamForm
from teams.models import Team, Membership, WaitList
from users.models import User
from projects.models import Project
from django.shortcuts import render

def join_team(request, team_id):
    wait_member = request.user
    team = Team.objects.get(id=team_id)
    WaitList.objects.create_wait_list(team, wait_member)
    return HttpResponse("OK")

def search_team(request):
    search_team = request.GET['search_team']
    pattern_not_found = "that pattern not found in Team list"

    # Case insensitive filtering
    teams = Team.objects.filter(name__icontains = search_team) 
    print teams
    
    return render(
               request,
               "teams/search_team_result.html",
               { "teams" : teams },
           )            

class MakeTeamView(FormView):
    template_name = "teams/maketeam.html"
    form_class = MakeTeamForm

    def form_valid(self, form):
        team_invalid = "ERROR : invalid team name"
        team_already_exist = "ERROR : The team name already exists"
        team_make_success = "Team created successfully"

        # name field required 
        name = self.request.POST["teams_team_name"]
        
        # valid team name test
        try:
            Team.objects.validate_name(name)
        except ValidationError:
            messages.error(self.request, team_invalid)
            return HttpResponseRedirect(reverse("teams:maketeam")) 

        # unique team test
        try:
            Team.objects.get(name = name)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, team_already_exist)
            return HttpResponseRedirect(reverse("teams:maketeam"))          
 
        # Login check is programmed in buildbuild/urls.py
        # link user to team using Membership  
        user = self.request.user
        team = Team.objects.create_team(name)

        membership = Membership.objects.create_membership(
            team = team, 
            user = user, 
        )
        membership.is_admin = True
        membership.save()

        messages.success(self.request, team_make_success)
 
        return HttpResponseRedirect(reverse("home"))

