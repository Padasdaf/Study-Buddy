from django.shortcuts import render
from django.views.generic.base import TemplateView
from homepage.models import User  
import pandas as pd 
import json
from django.http import JsonResponse
import os
from matchingalgorithm import LabelEncoder


class HomeView(TemplateView):
    template_name = 'studbud/homepage.html'

class BuddiesView(TemplateView):
    template_name = 'studbud/buddies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all users from the UserProfile model
        users = User.objects.all()

        # Example of fitting LabelEncoders with expected categories for each field
        label_encoders = {
            'gender': LabelEncoder(),
            'personality': LabelEncoder(),
            'preferred_study_time': LabelEncoder(),
            'learning_style': LabelEncoder()
        }

        # Fit label encoders with actual categories (adjust as needed)
        label_encoders['gender'].fit(['Male', 'Female'])
        label_encoders['personality'].fit(['Introvert', 'Extrovert'])
        label_encoders['preferred_study_time'].fit(['Morning', 'Afternoon', 'Evening'])
        label_encoders['learning_style'].fit(['Visual', 'Auditory', 'Kinesthetic'])

        # Reverse the encoding for each user with error handling
        for user in users:
            try:
                user.gender = label_encoders['gender'].inverse_transform([user.gender])[0]
                user.personality = label_encoders['personality'].inverse_transform([user.personality])[0]
                user.preferred_study_time = label_encoders['preferred_study_time'].inverse_transform([user.preferred_study_time])[0]
                user.learning_style = label_encoders['learning_style'].inverse_transform([user.learning_style])[0]
            except ValueError as e:
                print(f"Skipping user {user.name} due to unseen label: {e}")

        # Add users to context
        context['users'] = users
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
        generated_users_df = pd.DataFrame(columns=['user_id', 'class', 'learning_style', 'personality', 'gender'])

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update the generated_users DataFrame."""
        try:
            print(f"CSV File Path: {self.csv_file_path}")  # Debug: print the file path
            data = json.loads(request.body)

            new_user_id = len(MatchupView.generated_users_df) + 1

            # Create a new DataFrame row from the form data
            new_row = pd.DataFrame({
                'user_id': [new_user_id],
                'class': [data.get('class', '')],
                'learning_style': [data.get('learning_style', '')],
                'personality': [data.get('personality', '')],
                'gender': [data.get('gender', '')],
                'preferred_study_time': [data.get('preftime', '')],
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