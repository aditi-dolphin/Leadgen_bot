import requests
import logging

logger = logging.getLogger(__name__)

url ="https://dev.api.civilcops.com/bot/v1/bot_user/8583062054"

Agent_ID ="8229c7918b814732a3f3278920528fed"
Agent_Access_Token = "88621a91a9084f41b4f301f5f9cb596d"

def call_api(url: str, data: dict, mode="get") -> list:
    """
    Input:
        1. URL: It should contains the URL for the API.
        2. Data: It should contains the payload to call the API.
        3. Mode: It should contain string specifying request mode.

    Process:
        This method is used to call API using the provided URL and the Data.

    Output:
        It return an object of list type which contains the true false based on status code received after calling the API and on second index
        it contains the data returned by the API.
    """
    headers = {"Authorization": f"Bearer {Agent_Access_Token}"}
    if mode == 'get':
        logger.info(f" url:{url}, data:{data}, header:{header}")
        response = requests.get(url=url, data=data, headers=headers)
    if mode == 'post':
        response = requests.post(url=url, data=data, headers=headers)
    if mode == 'patch':
        response = requests.patch(url=url, data=data, headers=headers)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, {}
        

def save_customer_details(sender_id: str, data: dict, mode: str, channel=None) -> bool:
    """
    Input:
        1. SenderID: It should contain the SenderID.
        2. Data: It contains the payload to call the API.
        3. Mode: Add/Edit
        4. Channel: it should contain rest API channel.

    Process:
        This method is used to save the customers detail using API.

    Output:
        It return a boolean value.
    """
    if mode == "Add":
        data["sender_id"] = sender_id
        data["agent_id"] = Agent_ID
        data["channel"] = channel
        
        response = call_api(f'https://dev.api.civilcops.com/bot/v1/bot_user', data, "post")
    else:
        response = call_api(f'https://dev.api.civilcops.com/bot/v1/bot_user/{sender_id}', data,  "patch")
    return response[0]

