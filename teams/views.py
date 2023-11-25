from rest_framework.views import APIView, status, Request, Response
from .models import Team
from django.forms import model_to_dict
from utils import data_processing
from exceptions import InvalidYearCupError, ImpossibleTitlesError, NegativeTitlesError

class TeamView(APIView):
     def post(self, req: Request) -> Response:
        try:
            data_processing(req.data)
            team = Team.objects.create(**req.data)
            converted_team = model_to_dict(team)
            return Response(converted_team, status.HTTP_201_CREATED) 
        except NegativeTitlesError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)
     
     def get(self, req: Request) -> Response:
        teams = Team.objects.all()
        converted_teams = []
        for team in teams:
            converted_teams.append(model_to_dict(team))
        return Response(converted_teams, status.HTTP_200_OK)
    
class TeamDetailView(APIView):
    def get(self, req: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        converted_team = model_to_dict(found_team)
        return Response(converted_team, status.HTTP_200_OK)

    def delete(self, req: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        found_team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, req: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        for k, v in req.data.items():
            setattr(found_team, k, v)
        found_team.save()
        converted_team = model_to_dict(found_team)
        return Response(converted_team, status.HTTP_200_OK)
