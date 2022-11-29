# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction, logger
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from datetime import datetime

import requests
import json


class ClearSlotValues(Action):

    def name(self) -> Text:
        return "action_clear_slot_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]


class AddTodoAction(Action):
    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        todo = tracker.get_slot("todo")

        url = "http://localhost:4000/add_todo"
        payload = {
            "body": todo
        }
        headers = {
            'Content-Type': 'application/json'
        }

        logger.debug("Payload: {}".format(payload))

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        logger.debug("Response: {}".format(response.text))

        if response.status_code == 200:
            dispatcher.utter_message(text="todo added!")
        else:
            dispatcher.utter_message(
                text="failed to add todo! sorry bestie :(")

        return []


class AddTodoActionValidation(FormValidationAction):

    def name(self) -> Text:
        return "validate_todo_form"

    def validate_todo(self, value, dispatcher, tracker, domain):

        return {"todo": value}


class GetTodosAction(Action):
    def name(self) -> Text:
        return "action_get_todos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        timeframe = tracker.get_slot("timeframe")

        url = "http://localhost:4000/get_todos"
        payload = {
            "timeframe": timeframe
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:

            response = json.loads(response.text)

            output = ""
            for todo in response['message']:

                temp = todo['id'] + " - " + todo['body'] + " - "
                if todo['status']:
                    temp += "completed"
                else:
                    temp += "uncomplete"

                output += temp + "\n"

            if output == "":
                output = "You have no todos.... Chill bestie :)"
            else:
                output = "here's a list of things you should do... \n" + output

            dispatcher.utter_message(text=output)
        else:
            dispatcher.utter_message(
                text="failed to show todo! sorry bestie :(")

        return []


class GetTodosValidation(FormValidationAction):

    def name(self) -> Text:
        return "validate_get_todos_form"

    def validate_timeframe(self, value, dispatcher, tracker, domain):

        return {"timeframe": value}


class MarkTodoAction(Action):
    def name(self) -> Text:
        return "action_mark_todo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.get_slot("id")

        url = "http://localhost:4000/mark_todo"
        payload = {
            "id": id
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:

            response = json.loads(response.text)

            output = ""
            for todo in response['message']:

                temp = todo['id'] + " - " + todo['body'] + " - "
                if todo['status']:
                    temp += "completed"
                else:
                    temp += "uncomplete"

                output += temp + "\n"

            if output == "":
                output = "You have no todos.... Chill bestie :)"
            else:
                output = "ok here's your updated list... \n" + output

            dispatcher.utter_message(text=output)
        else:
            dispatcher.utter_message(
                text="failed to mark todo! sorry bestie :(")

        return []


class MarkTodoValidation(FormValidationAction):

    def name(self) -> Text:
        return "validate_mark_todo_form"

    def validate_id(self, value, dispatcher, tracker, domain):

        return {"id": value}
