#!/usr/bin/env python

from generate_team_players import generate_team_players
from generate_game_statistics import generate_game_statistics
from generate_season_statistics import generate_season_statistics

la_salle_team_id = "75674569-9493-4636-827c-dd9788f93423"
clackamas_jv_team_id = "aff3ed7e-b4ce-53d8-9cb3-42cf365620c5"
clackamas_varsity_team_id = "7d2150b9-8a73-524c-9a96-3d5e7e90b68d"
madlax_team_id = "f31cd914-3936-5d8f-9412-293c55886432"

madlax_player_ids = ["bee6c7d3-52b0-4093-af31-609c43df8f4b"]

clackamas_jv_player_ids = [
    "4e7486d1-7586-5621-bf51-f1c9e232d2d3",
    "6a6bfc42-41f8-5b48-b5fa-1f96b9c2a0ff",
    "2ba7e33d-e1ce-5781-b67b-d180e4f2c0ce",
    "7061148e-e7d3-57a1-813e-67589050ead6",
    "6a27a5d5-e9ab-5924-b1b4-e298171c8a73",
    "e3d45a83-3b7d-5f61-ad6b-79de37afff37",
    "02bcf8fb-f1ba-5a97-b9a8-91ea0a012e83",
    "aab397fd-cc71-5582-aef8-3bdeb317cf2b",
    "117b4917-a790-5adc-8019-5d7d8c726aa4",
    "5b568ba6-d93f-5b47-a024-9ec0207b1b86",
    "8d421db7-b73f-552c-acf9-504208f85d19",
    "2d9ceefb-af5f-53b7-967d-7b52f44dc6a8",
    "e3fc5e81-2d96-5b51-a025-d16170b8d373",
    "e0bf2f79-61e7-54d9-b467-93896096b25c",
    "58e75c2a-53de-54ec-85bb-4da12e942401",
    "5d3fcfd3-7695-5593-b4ff-f645fb2914d8",
    "0374960d-3806-5823-9b68-32e7f8afb3a9",
    "87ac6fa6-02b0-5d65-9e91-df7fbfcd0e6c",
    "67e0c3ea-4321-5a72-a88b-4d8863b4833f"
]

clackamas_varsity_player_ids = [
    "6a6bfc42-41f8-5b48-b5fa-1f96b9c2a0ff",
    "2ba7e33d-e1ce-5781-b67b-d180e4f2c0ce",
    "e3d45a83-3b7d-5f61-ad6b-79de37afff37",
    "02bcf8fb-f1ba-5a97-b9a8-91ea0a012e83",
    "aab397fd-cc71-5582-aef8-3bdeb317cf2b",
    "5b568ba6-d93f-5b47-a024-9ec0207b1b86",
    "8d421db7-b73f-552c-acf9-504208f85d19",
    "2d9ceefb-af5f-53b7-967d-7b52f44dc6a8",
    "e0bf2f79-61e7-54d9-b467-93896096b25c",
    "5d3fcfd3-7695-5593-b4ff-f645fb2914d8",
    "fd2ea909-10f5-5c06-84b7-dd8e033c9c1f",
    "78fc3d43-8a93-5c36-805c-94bfd501f18f",
    "ee3e9f81-b028-59ef-bad1-80ee56e81dbd",
    "19386a2c-512c-5ee7-8388-83a30cd49d79",
    "1d4c6aef-12a3-5598-ae40-7be09f273b99",
    "08bbd111-5d31-55cf-8ba3-458530efed60",
    "6f964126-0ad4-5a0f-9991-67e9b8df0708",
    "f2706293-73bb-53ee-99a6-761eae6c36e4",
    "61617eb7-5252-523b-a5dd-bc10c0d84cb7",
    "c05f6019-a865-5b0a-b9fd-72702cd6e5e6",
    "28f5b610-9df6-5c68-af61-5ddd22b3e4ed"
]

la_salle_player_ids = [
    "bee6c7d3-52b0-4093-af31-609c43df8f4b",
    "0a13600b-bd52-428f-9cd3-70d2426ac79a",
    "937f20d0-27f5-4d07-b985-0a080046af02",
    "8bb0bcb4-9429-4c82-8898-cfd8a275130f",
    "271d2693-ee38-4bae-aacc-de8debc949d5",
    "08378719-076a-450b-9f54-e06e3d2acf99",
    "a6c31cfd-afe1-4aa9-a67b-dc7137ea7908",
    "950cb035-6fae-4ea4-8f07-191c5a3fbad7",
    "3f0102ee-3ee6-47f2-97d2-275105026006",
    "834f0046-4f4c-4c62-9027-c98b6d1c618f",
    "c17e71a2-efbc-4447-be78-ff481423bcc4",
    "61444ae9-cff9-4cc3-bf17-1221724ba8db",
]

game_ids = [
    "c12dc2ba-6572-46b8-95df-75da8b1b4baf",
    "1d9fd779-cfcc-4207-a3ae-f1fcbb41dce2",
    "ab1fdb62-2e8c-47a4-88b4-2b95738df66c",
    "cb2d9902-5461-44b6-9a1b-ffda73429239",
    "b84dadae-38bb-4b39-9b3f-067fcab39f91",
    "8bd5e0c2-03cb-4102-a575-7dd9022801f9",
    "6381dc57-77a8-47c9-a7af-fa1ad9e4df5d",
    "212700dd-1fa3-4e37-857d-7a84c782234f",
    "e54ef386-b480-437d-9849-2422e3c34fa8",
    "a2ac224e-b347-4443-8f47-1f65553935bf",
    "adf60a1f-d9d6-4981-baa1-490ccecd77b0",
    "c7ef8df7-a1bf-4306-bed8-e8e4585a43cd",
    "c13d1f7c-a70e-40d7-9dcc-f6ba29f3201b",
    "4cb55c98-f6b1-480b-9bef-cfa1409247b8",
    "836c7525-c4a2-467b-9e3d-2c4a8bb631ea",
    "b689dfbe-570f-4709-87d6-179c1dbdd345",
]

# print(
#     generate_season_statistics(
#         [(madlax_team_id, player_id) for player_id in madlax_player_ids], 2018
#     )
# )


# for game_id in game_ids:
#     print(f"game_id: {game_id}:\n{generate_game_statistics(game_id, la_salle_player_ids)}")


print(generate_team_players(clackamas_jv_team_id, clackamas_jv_player_ids))

print ("var --")
print(generate_team_players(clackamas_varsity_team_id, clackamas_jv_player_ids))