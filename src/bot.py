import requests
import json
import time

URL = "https://fr20.herozerogame.com/request.php" #Change to your server

DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://fr20.herozerogame.com", #Change to your server
    "referer": "https://fr20.herozerogame.com/", #Change to your server
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

DEFAULT_BODY = {
    "user_id": 1402, #Change to your user id
    "user_session_id": "8LviJ4hQ2bxP9FI8wXKFvd0oDgywUU", #Change to your user session id
    "client_version": "html5_232",
    "auth": "9776fcfd1f0a2c20284e89850b81764d", #Change every time you refresh the page but works even not changed
    "rct": 1,
    "keep_active": "true",
    "device_type": "web"
}

COOLDOWN = 5

def get_quests():
    response = requests.post(URL, headers=DEFAULT_HEADERS, data={
        "existing_session_id": DEFAULT_BODY["user_session_id"],
        "existing_user_id": DEFAULT_BODY["user_id"],
        "client_id": "fr201729799812",
        "app_version": 232,
        "action": "autoLoginUser",
        "user_id": 0,
        "user_session_id": 0,
        "client_version": DEFAULT_BODY["client_version"],
        "auth": DEFAULT_BODY["auth"],
        "rct": DEFAULT_BODY["rct"],
        "keep_active": DEFAULT_BODY["keep_active"],
        "device_type": DEFAULT_BODY["device_type"]
    })
    data = response.json()["data"]
    return data["quests"]

def get_max_xp_ratio_quest():
    quests = get_quests()
    best_quest = quests[0]
    best_quest_ratio = get_quest_rewards(best_quest)["xp"] / best_quest["energy_cost"]

    for quest in quests:

        quest_rewards =  get_quest_rewards(quest)
        quest_ratio = quest_rewards["xp"]/quest["energy_cost"]

        if quest_ratio > best_quest_ratio:
            best_quest = quest
            best_quest_ratio = quest_ratio

    return best_quest

def get_quest_by_id(quest_id):
    quests = get_quests()
    for quest in quests:
        if quest["id"] == quest_id:
            return quest

def get_quest_rewards(quest):
    return json.loads(quest["rewards"])

def start_quest(quest_id):
    quest = get_quest_by_id(quest_id)
    quest_rewards = get_quest_rewards(quest)
    response = requests.post(URL, headers=DEFAULT_HEADERS, data={
        "quest_id": quest_id,
        "action": "startQuest",
        **DEFAULT_BODY
    })
    response_json = response.json()
    if response_json["error"] == "":
        print(f"Quest {quest_id} launched successfully. "
              f"XP: {quest_rewards['xp']}, "
              f"Coins: {quest_rewards['coins']}, "
              f"Energy: {quest['energy_cost']}")
    else:
        print(f"Unable to start quest {quest_id}")
        print(response_json)

def start_best_xp_ratio_quest():
    best_xp_ratio_quest = get_max_xp_ratio_quest()
    start_quest(best_xp_ratio_quest["id"])

def check_for_quest_complete():
    response = requests.post(URL, headers=DEFAULT_HEADERS, data={
        "quest_id": 0,
        "action": "checkForQuestComplete",
        **DEFAULT_BODY
    })
    response_json = response.json()
    if response_json["error"] == "":
        print("Quest completed successfully verified")
    else:
        print("Unable to verify quest completion")
    return response.json()

def claim_quest_rewards():
    response = requests.post(URL, headers=DEFAULT_HEADERS, data={
        "discard_item": "false",
        "refresh_inventory": "false",
        "action": "claimQuestRewards",
        **DEFAULT_BODY
    })
    response_json = response.json()
    if response_json["error"] == "":
        print("Quest reward successfully collected")
    else:
        print("Unable to collect quest reward")
    return response.json()

def auto_xp():
    while True:
        best_xp_ration_quest = get_max_xp_ratio_quest()
        start_best_xp_ratio_quest()
        print(f"Waiting {best_xp_ration_quest['duration'] / 60} min")
        time.sleep(best_xp_ration_quest['duration'] + COOLDOWN)
        check_for_quest_complete()
        claim_quest_rewards()
        time.sleep(COOLDOWN)