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

from django.db import IntegrityError
from django.db import OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from teams.forms import MakeTeamForm
from teams.models import Team, Membership, WaitList
from users.models import User

class MakeTeamView(FormView):
    template_name = "teams/maketeam.html"
    form_class = MakeTeamForm

    def form_valid(self, form):
        def msg_error(msg=""):
            messages.add_message(
                self.request,
                messages.ERROR,
                msg
            )

        def msg_success(msg=""):
            messages.add_message(
                self.request,
                messages.SUCCESS,
                msg
            )

        team_invalid = "ERROR : invalid team name"
        team_already_exist = "ERROR : The team name already exists"
        team_make_success = "Team created successfully"

        # name field required 
        name = self.request.POST["teams_team_name"]
        
        # valid team name test
        try:
            Team.objects.validate_name(name)
        except ValidationError:
            msg_error(team_invalid)
            return HttpResponseRedirect(reverse("maketeam"))          

        # unique team test
        try:
            Team.objects.get(name = name)
        except ObjectDoesNotExist:
            pass
        else:
            msg_error(team_already_exist)
            return HttpResponseRedirect(reverse("maketeam"))          
 
        # Login check is programmed in buildbuild/urls.py
        # link user to team using Membership  
        user = self.request.user
        team = Team.objects.create_team(name)

        membership = Membership.objects.create(
            team = team, 
            member = user, 
            is_admin = True,
        )
        membership.save()

        msg_success(team_make_success)
 
        return HttpResponseRedirect(reverse("home"))

