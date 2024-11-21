from django.shortcuts import render
from django.views.generic.base import TemplateView
from homepage.models import User  
import pandas as pd 
import json
from django.http import JsonResponse
import os

# Use this if you have a custom User model
# from django.contrib.auth.models import User  # Use this if you're using Django's built-in User model

class HomeView(TemplateView):
    template_name = 'studbud/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_users'] = User.objects.all()
        return context

class LoginView(TemplateView):
    template_name = 'studbud/login.html'

class ProfileView(TemplateView):
    template_name = 'studbud/profile.html'

class HistoryView(TemplateView):
    template_name = 'studbud/history.html'

class FeedbackView(TemplateView):
    template_name = 'studbud/feedback.html'

class MatchupView(TemplateView):
    template_name = 'studbud/matchup.html'

    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
    'generated_users.csv')
    
    try:
        generated_users_df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        generated_users_df = pd.DataFrame(columns=['user_id', 'course_code', 'learning_style', 'personalities', 'gender'])

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update the generated_users DataFrame."""
        try:
            print(f"CSV File Path: {self.csv_file_path}")  # Debug: print the file path
            data = json.loads(request.body)

            new_user_id = len(MatchupView.generated_users_df) + 1

            # Create a new DataFrame row from the form data
            new_row = pd.DataFrame({
                'user_id': [new_user_id],
                'course_code': [data.get('class', '')],
                'preferred_study_time': [data.get('preftime', '')],
                'learning_style': [data.get('learning_style', '')],
                'personalities': [data.get('personality', '')],
                'gender': [data.get('gender', '')]
            })

            # Append the new row to the existing DataFrame
            MatchupView.generated_users_df = pd.concat(
                [MatchupView.generated_users_df, new_row], ignore_index=True
            )

            # Save the updated DataFrame to the CSV file
            MatchupView.generated_users_df.to_csv(self.csv_file_path, index=False)

            return JsonResponse({'status': 'success', 'message': 'Data successfully added to CSV!', 'data': data})
        except Exception as e:
            # Return a JSON response with the error message
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)