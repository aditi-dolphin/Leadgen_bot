# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union, Optional
import logging
import spacy
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import Restarted, EventType, SlotSet, FollowupAction, AllSlotsReset
import requests
import json
from configuration.facebook import fb_access_token
from templates.quick_replies import add_quick_reply
from InternalAPI import save_customer_details
from templates.buttons import ButtonTemplate

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_lg")

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info(f"action {self.name()} called")    
        save_customer_details(tracker.sender_id, {},
                              'Add', tracker.get_latest_input_channel())
        dispatcher.utter_message("Welcome to the Bot powered by DolphinChat")  
        return []


class Leadform(FormAction):
    def __init__(self):
        self.Valid = True

    def name(self) -> Text:
        return "lead_form"
   
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", "phone_number", "email_address"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        return{
            "name": [
             self.from_text()
          ],
            "phone_number":[
             self.from_text()
          ],
            "email_address":[
             self.from_text()
          ],
        }

    def validate_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate name."""
        logger.info(f"input from user: {value}")
        text = nlp(value)
        name = list()
        for entity in text.ents:
            if entity.label_ == "PERSON":
                name.append(entity.text)
        logger.info(f"entities found : {name}")
        if not name:
            save_customer_details(tracker.sender_id,{
            "name": name}, "Edit", tracker.get_latest_input_channel())
            self.Valid = False
            return {
               "name": None
            }
        return {
            "name": "  ".join(name)
        }

    def validate_phone_number(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone number."""

        text = value
        phone_number = ""
        for digit in text:
            if digit.isdigit():
                phone_number += digit
        if len(phone_number) <= 9:
            self.Valid = False
            save_customer_details(tracker.sender_id, {"phone_number": phone_number[-10:]}, "Edit",
                                  tracker.get_latest_input_channel())
                                
            return {
               "phone_number": None
            }
        else:
            return{
                "phone_number" : phone_number[-10:]
            }
        
    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate Email"""

        doc = nlp(value)
        for token in doc:
            if token.like_email:
                save_customer_details(tracker.sender_id, {"email_address": token.text}, "Edit",
                                      tracker.get_latest_input_channel())

                return {
                    "email": token.text
                }
        self.Valid = False
        return {
            "email": None
        }
    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        NameTemplate = ""
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if self.Valid:
                    NameTemplate = "utter_ask_"
                else:
                    NameTemplate = "utter_ask_again_"
                    self.Valid = True
                dispatcher.utter_message(template=f"{NameTemplate}{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

            # no more required slots to fill
        return None


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        name = tracker.get_slot("name")
        phone_number = tracker.get_slot("phone_number")
        email_address = tracker.get_slot('email_address')
        text = "Thankyou! Your response have been recorded.Someone from our team will get in touch with you shortly."
    # utter submit response
        dispatcher.utter_message(text=text)
        return [AllSlotsReset()]
