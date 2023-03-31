# Requires scryfall bulk-data json file to parse through.
# Gets the image and price associated with card.

import requests
import json

with open("unique-artwork-20230330210442.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    card_list = []
    image_counter = 1
    column_names = ["CID", "name", "legalites (commander)", "type", "main_type" 
                    "colors","color_identity", "mana_cost", "set_name","rarity", "prices"]

    for card in data:

        # ["CMR", "MH1", "MH2", "THS", "ELD", "WAR", "GRN", "RNA", "AVR"]
        if card["set"] in ["cmr"]:

            card_parse_data = {}

            card_parse_data["CID"] = str(image_counter)
            card_parse_data["name"] = card["name"]
            card_parse_data["commander_legality"] = card["legalities"]["commander"]

            type_card = [types.split() for types in card.split("—")]

            card_parse_data["type"] = card["type_line"]
            card_parse_data["main_tpye"] = type_card[0]
            card_parse_data["colors"] = card["colors"]
            card_parse_data["color_identity"] = card["color_identity"]
            card_parse_data["mana_cost"] = card["mana_cost"]
            card_parse_data["set_name"] = card["set_name"]
            card_parse_data["rarity"] = card["rarity"]

            if card["prices"]["usd"] is not None:
                card_parse_data["price"] = card["prices"]["usd"]

            elif card["prices"]["usd_foil"] is not None:
                card_parse_data["price"] = card["prices"]["usd_foil"]
            
            elif card["prices"]["usd_etched"] is not None:
                card_parse_data["price"] = card["prices"]["usd_etched"]
            
            else:
                card_parse_data["price"] = "0.00"

            card_list.append(card_parse_data)

            picture_var = requests.get(card["image_uris"]["normal"])
            picture = open(f"Magic_pictures/{image_counter}.jpg", "wb")
            picture.write(picture_var.content)
            picture.close()

            image_counter += 1

    with open("prices.txt", "w", encoding="utf-8") as parse_file:

        for index, card_data in enumerate(card_list, 1):

            for data in card_data:
                if (index == len(card_data)):
                    parse_file.write(f"{card_data["CID"]};")

                else:
                    parse_file.write(f"{card_data["CID"]}\n")


