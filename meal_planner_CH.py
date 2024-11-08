import requests
import pandas as pd
import logging
from keys import EDAMAM_APP_ID, EDAMAM_APP_KEY

EDAMAM_URL = 'https://api.edamam.com/search' # https://api.edamam.com/api/recipes/v2

def generate_meal_plan(dietary_preferences, health_goals):
    params = {
        'q': 'healthy',
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_APP_KEY,
        'diet': dietary_preferences,
        'from': 0,
        'to': 5
    }

    try:
        logging.info("Sending request to Edamam API")
        response = requests.get(EDAMAM_URL, params=params)
        response.raise_for_status()
        data = response.json()

        meal_plan = []
        for recipe in data['hits']:
            meal_plan.append({
                'name': recipe['recipe']['label'],
                'ingredients': recipe['recipe']['ingredientLines'],
                'calories': recipe['recipe']['calories']
            })

        # Save meal plan to CSV file
        meal_plan_df = pd.DataFrame(meal_plan)
        meal_plan_df.to_csv('./data/meal_plan.csv', index=False)
        
        logging.info("Meal plan successfully generated and saved to CSV")
        return meal_plan_df

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching recipes: {e}")
        return pd.DataFrame()
    

