# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# actions.py

# -------------------------
# Custom Actions for Rasa
# -------------------------

from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
import requests
import random
from typing import Any, Dict, List

BASE_URL = "https://touristeproject.onrender.com"
# -------------------------
# Action to Get All Attractions
# -------------------------
class ActionGetAllAttractions(Action):
    def name(self):
        return "action_get_all_attractions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        try:
            # Appel API
            response = requests.get("https://touristeproject.onrender.com/api/public/getAll/Attraction")

            if response.status_code == 200:
                data = response.json()
                if not data:
                    dispatcher.utter_message(text="No attraction is found.")
                else:
                    attractions = [item.get("name", "Inconnue") for item in data][:5]
                    msg = "Here are some avialable attractions  :\n" + "\n".join(f"- {name}" for name in attractions)
                    dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="Error while recupering attractions.")
        except Exception as e:
            dispatcher.utter_message(text="Une erreur est survenue en appelant l'API.")
            print(e)

        return []

# -------------------------
# Action to Get Random Attractions
# This action fetches a random selection of attractions from the API.
# -------------------------

class ActionGetRandomAttractions(Action):
    def name(self) -> str:
        return "action_get_random_attractions"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        try:
            response = requests.get("https://touristeproject.onrender.com/api/public/getAll/Attraction")

            if response.status_code != 200:
                dispatcher.utter_message(text="Error while recupering attractions.")
                return []

            data = response.json()

            if not data:
                dispatcher.utter_message(text="No attraction is found.")
                return []

            # 🔀 Tirer 5 attractions aléatoires (ou moins si < 5)
            sample_size = min(5, len(data))
            random_attractions = random.sample(data, sample_size)

            names = [item.get("name", "Sans nom") for item in random_attractions]

            msg = "Here are some attractions to discover :\n" + "\n".join(f"- {n}" for n in names)
            dispatcher.utter_message(text=msg)

        except Exception as e:
            print(f"[ERREUR] Appel API : {e}")
            dispatcher.utter_message(text="Une erreur est survenue en consultant l’API.")

        return []

# -------------------------
# Action pour obtenir tous les hôtels
# -------------------------

class ActionGetAllHotels(Action):
    def name(self) -> str:
        return "action_get_all_hotels"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        try:
            response = requests.get("https://touristeproject.onrender.com/api/public/getAll/Amenities")

            if response.status_code != 200:
                dispatcher.utter_message(text="Error while recupering amenities.")
                return []

            data = response.json()

            if not data:
                dispatcher.utter_message(text="None amenity is found.")
                return []

            # 🔀 Tirer 5 attractions aléatoires (ou moins si < 5)
            sample_size = min(5, len(data))
            random_attractions = random.sample(data, sample_size)

            names = [item.get("name", "Sans nom") for item in random_attractions]

            msg = "Here are some amenities to discover :\n" + "\n".join(f"- {n}" for n in names)
            dispatcher.utter_message(text=msg)

        except Exception as e:
            print(f"[ERREUR] Appel API : {e}")
            dispatcher.utter_message(text="Une erreur est survenue en consultant l'API.")

        return []

# --------------------------------------------
# Action pour obtenir les accommodation par randomly
# --------------------------------------------

class ActionGetRandomAttractions(Action):
    def name(self) -> str:
        return "action_get_random_accommodations"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        try:
            response = requests.get("https://touristeproject.onrender.com/api/public/getAll/Amenities")

            if response.status_code != 200:
                dispatcher.utter_message(text="Error while recupering  amenities.")
                return []

            data = response.json()

            if not data:
                dispatcher.utter_message(text="None amenity is found.")
                return []

            sample_size = min(5, len(data))
            random_aminities = random.sample(data, sample_size)

            names = [item.get("name", "Without name") for item in random_aminities]

            msg = "Here are some amenities to discover :\n" + "\n".join(f"- {n}" for n in names)
            dispatcher.utter_message(text=msg)

        except Exception as e:
            print(f"[ERREUR] Appel API : {e}")
            dispatcher.utter_message(text="Une erreur est survenue en consultant l'API.")

        return []

# -------------------------
# Action pour obtenir les attractions par type
# -------------------------

ENDPOINT_BY_TYPE = {
    "natural": f"{BASE_URL}/api/public/NaturalAttractions",
    "historical": f"{BASE_URL}/api/public/HistoricalAttractions",
    "cultural": f"{BASE_URL}/api/public/CulturalAttractions",
    "artificial": f"{BASE_URL}/api/public/ArtificialAttractions",
}

class ActionGetAttractionsByType(Action):
    def name(self) -> str:
        return "action_get_attractions_by_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        type_requested = (tracker.get_slot("type_attraction") or "").lower()

        # 1️⃣ Vérifie que le type demandé est supporté
        if type_requested not in ENDPOINT_BY_TYPE:
            dispatcher.utter_message(text="I don't seems like I know that type of attraction. Please choose from: natural, historical, cultural, or artificial.")
            return []

        url = ENDPOINT_BY_TYPE[type_requested]

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                dispatcher.utter_message(text="The service is not responding.")
                return []

            data = resp.json()

            if not data:
                dispatcher.utter_message(text=f"None {type_requested} attraction is found.")
                return []

            # Limite à 5 résultats pour ne pas noyer l’utilisateur
            names = [item.get("name", "Sans nom") for item in data][:5]
            msg = f"Here are somme {type_requested} attractions :\n" + "\n".join(f"- {n}" for n in names)
            dispatcher.utter_message(text=msg)

        except Exception as e:
            print(f"[ActionGetAttractionsByType] API error: {e}")
            dispatcher.utter_message(text="Une erreur est survenue en consultant l’API.")

        return []
