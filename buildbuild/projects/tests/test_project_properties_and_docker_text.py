from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from projects.views import MakeProjectView
from projects.models import Project

from teams.models import Team
from users.models import User
from buildbuild import custom_msg


class MakeProjectPageTest(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.client = Client()
        self.project_name = "buildbuild_project"
        self.team_name = "buildbuild_team"
        self.second_team_name = "must_be_created_by_post_method"
        self.lang_python = "python"
        self.lang_python_upper_case = "PYTHON"
        self.ver_278 = "2.7.8"
        self.invalid_lang = "never_exist_language"
        self.invalid_ver = "never_exist_version"

        self.user_email = "test@example.com"
        self.user_password = "test_password"
        
        self.TEST_SERVER_URL = "http://testserver"

        self.user = User.objects.create_user(
            email = self.user_email,
            password = self.user_password,
        )

        self.docker_text_with_python_278 = \
            Project.objects.customize_docker_text(self.lang_python, self.ver_278)

    # Default Set function, These are not Unit Test function
    def post_login_set(self, user_email="", user_password="", follow = False):
        response = self.client.post(
                       "/users/login/", {
                           "email" : user_email,
                           "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Default Set function, These are not Unit Test function
    def post_make_team_set(self, team_name="", follow=False):
        response = self.client.post(
                       "/teams/maketeam/", {
                       "teams_team_name": team_name,
                       },
                       follow = follow
                   )
        return response

    # Default Set function, These are not Unit Test function
    def post_make_project_set(self, name="", team_name="", follow=False, **kwargs):

        if "properties" in kwargs:
            properties = kwargs["properties"]
            response = self.client.post(
                           "/projects/makeproject/", {
                               "projects_project_name" : name,
                               "projects_team_name" : team_name,
                               "lang" : properties['language'],
                               "ver" : properties['version'],
                           },
                           follow = follow
                       )
        else:
            response = self.client.post(
                           "/projects/makeproject/", {
                               "projects_project_name" : name,
                               "projects_team_name" : team_name
                           },
                           follow = follow
                       )
        return response

    def test_post_project_with_invalid_language_error_message_and_should_redirect_to_makeproject(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name, follow = True)
        response = self.post_make_project_set(
                       name = self.project_name, 
                       team_name = self.team_name, 
                       properties = {
                                        'language' : self.invalid_lang,
                                        'version' : self.ver_278
                                    },
                       follow = True
                   )
        self.assertRedirects(response, "/projects/makeproject/")
        self.assertContains(response, custom_msg.project_lang_invalid)

    def test_post_project_with_invalid_version_error_message_and_should_redirect_to_makeproject(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name, follow = True)
        response = self.post_make_project_set(
                       name = self.project_name, 
                       team_name = self.team_name, 
                       properties = {
                                        'language' : self.lang_python, 
                                        'version' : self.invalid_ver
                                    },
                       follow = True
                   )
        self.assertRedirects(response, "/projects/makeproject/")
        self.assertContains(response, custom_msg.project_ver_invalid)
    
    def test_post_project_docker_text_must_be_equal_to_the_result_of_customize_docker_text_function_in_models(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name, follow = True)
        self.post_make_project_set(
            name = self.project_name, 
            team_name = self.team_name, 
            properties = {
                             'language' : self.lang_python, 
                             'version' : self.ver_278
                         },
            follow = True,
        )

        # For travis test, get using name instead of get id
        project = Project.objects.get(name = self.project_name)
        self.assertEqual(project.docker_text, self.docker_text_with_python_278)
    


