# Requires scryfall bulk-data json file to parse through.
# Gets the image and price associated with card.

import requests
import json
import os
from set_data import get_all_sets


def get_bulk_json():

    resp = requests.get("https://api.scryfall.com/bulk-data")

    if resp.status_code == 200:
        
        data = resp.json()
        json_obj = json.dumps(data, ensure_ascii=False, indent=4)

        try:
            dirname = os.path.dirname(__file__)
            json_dir = os.path.join(dirname, 'json-files')
            os.mkdir(json_dir, mode = 0o666)

        except FileExistsError:
                pass

        with open(os.path.join(json_dir, "data.json"), "w", encoding="utf-8") as json_file:
            json_file.write(json_obj)

        with open(os.path.join(json_dir, "data.json"), "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            
        for obj in json_data["data"]:
            
            if obj["name"] == "Unique Artwork":
                    bulk_data = requests.get(obj["download_uri"])

                    if bulk_data.status_code == 200:
                        bulk_data = bulk_data.json()
                        bulk_obj = json.dumps(bulk_data, ensure_ascii=False, indent=4)

                        with open(os.path.join(json_dir, "bulk_data_file.json"), "w", encoding="utf-8") as bulk_file:
                            bulk_file.write(bulk_obj)
                    
                    else:
                        print("Error from server: " + str(bulk_data.content))

    else:
        print("Error from server: " + str(resp.content))

def parse_bulk_json(download_cards):

    dirname = os.path.dirname(__file__)

    if download_cards:
        try:
            magic_dir = os.path.join(dirname, 'magic-cards')
            os.mkdir(magic_dir, mode = 0o666)

        except FileExistsError:
                pass

    with open(os.path.join(os.path.join(dirname, 'json-files'), "bulk_data_file.json"), "r", encoding="utf-8") as json_file:

        data = json.load(json_file)
        card_list = []
        image_counter = 1
        column_names = ["CID", "name", "format-commander", "type", "main_type",
                        "colors","color_identity", "mana_cost", "set_name","rarity", "prices"]

        for card in data:

            # ["CMR", "MH1", "MH2", "THS", "ELD", "WAR", "GRN", "RNA", "AVR"]
            if card["set"] in ["cmr"]:

                card_parse_data = {}

                card_parse_data["CID"] = str(image_counter)
                card_parse_data["name"] = card["name"]
                card_parse_data["commander_legality"] = card["legalities"]["commander"]

                type_card = [types.strip() for types in card["type_line"].split("—")]

                card_parse_data["type"] = card["type_line"]
                card_parse_data["main_tpye"] = type_card[0]
                card_parse_data["colors"] = "".join(["{" + color + "}" for color in card["colors"]])
                card_parse_data["color_identity"] = "".join(["{" + color + "}" for color in card["color_identity"]])
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

                if download_cards:
                    
                    picture_var = requests.get(card["image_uris"]["normal"])
                    with open(os.path.join(magic_dir, f"{image_counter}.jpg"), "wb") as picture:
                        picture.write(picture_var.content)

                image_counter += 1

        user_file_name = input("Enter a filename (do not include \".txt\"): ")

        with open(f"{user_file_name}.txt", "w", encoding="utf-8") as parse_file:
            
            header_string = ";".join(column_names)
            header_string = header_string[:-1]
            parse_file.write(header_string + "\n")

            for index, card_data in enumerate(card_list, 1):
                    
                    if (index == len(card_list)):
                        parse_file.write(f'{card_data["CID"]};{card_data["name"]};{card_data["commander_legality"]};{card_data["type"]};{card_data["main_tpye"]};'
                                        f'{card_data["colors"]};{card_data["color_identity"]};{card_data["mana_cost"]};{card_data["set_name"]};{card_data["rarity"]};'
                                        f'{card_data["price"]}')

                    else:
                        parse_file.write(f'{card_data["CID"]};{card_data["name"]};{card_data["commander_legality"]};{card_data["type"]};{card_data["main_tpye"]};'
                                        f'{card_data["colors"]};{card_data["color_identity"]};{card_data["mana_cost"]};{card_data["set_name"]};{card_data["rarity"]};'
                                        f'{card_data["price"]}\n')

def set_selection():
    all_sets = get_all_sets()
    value_list = ["Numbers", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    print("Pick the value the set starts with.")
    print("---------------------------------------------------\n")
    for index in range(0, 27):
        print(f"{index+1}. {value_list[index]}")
    try:
        user_input = input("Which selection? (number only): ")


def main():
    while True:
        want_bulk_json = input("Do you want the bulk json file to be downloaded? (y/n): ")
        if want_bulk_json in ['Y', 'y']:
            get_bulk_json()
            break

        elif want_bulk_json in ['N', 'n']:
            break

        else:
            print("Not a valid input.")
    
    while True:
        want_mtg_pictures = input("Do you want to download pictures? (y/n): ")
        if want_mtg_pictures in ['Y', 'y']:
            parse_bulk_json(True)
            break

        elif want_mtg_pictures in ['N', 'n']:
            parse_bulk_json(False)
            break
        
        else:
            print("Not a valid input.")


if __name__ == "__main__":
    main()
