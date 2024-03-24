import json


def read_database():
    try:
        with open('workpiece_templates.json') as file:
            templates_list = json.load(file)
    except FileNotFoundError:
        templates_list = {}
        with open('workpiece_templates.json', 'w') as file:
            json.dump(templates_list, file)
    print(templates_list)
    return templates_list


def save_database(templates_list):
    with open('workpiece_templates.json', 'w') as file:
        json.dump(templates_list, file)
    return
