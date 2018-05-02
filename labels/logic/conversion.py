from bson import CodecOptions, SON

function_handler2 = {
    'position': lambda position: "%s%s" % (get_command('position'), position),
    'config': lambda object: get_config_info(object),
    'elements': lambda object: get_elements_info(object),
    'content': lambda object: "%s^FS" % object,
    'default': lambda object: get_command(object)
}

translations_dictionary = {
    "start": "XA",
    "close": "XZ",
    "origin": "LH",
    "encoding": "CI",
    "block": "FB",
    "text": "FD",
    "position": "FO",
    "image": "GFA"
}

label_json = {
    "type": "GIFTBOX",
    "config": {
            "coordinates_origin": "0,0",
            "encoding": "28",
    },
    "elements": [
        {
            "type": "block",
            "config": {
                "parameters": {
                    "width": "250",
                    "max_lines": "1",
                    "space_between_lines": "0",
                    "justification": "C",
                },
                "position": "20,50"
            },
            "elements": [
                {
                    "type": "text",
                    "content": "Texto de prueba"
                }
            ]
        },
        {
            "type": "block",
            "config": {
                "parameters": {
                    "width": "250",
                    "max_lines": "1",
                    "space_between_lines": "0",
                    "justification": "C",
                },
                "position": "20,80"
            },
            "elements": [
                {
                    "type": "text",
                    "content": "Texto de prueba f2"
                }
            ]
        },
        {
            "type": "image",
            "config": {
                "position": "20,200"
            },
            "content": "LABORATORY_GIFTBOX_X"
        }
    ]
}


def get_label(mongo, label_type):
    options = CodecOptions(document_class=SON)
    labels_collection = mongo.db.labels.with_options(codec_options=options)
    stored_label = labels_collection.find_one(
        {"type": label_type}, {'_id': False}
    )

    label = read_object(stored_label)
    label += get_command('close')

    return label


def get_command(key):
    command = "^%s" % translations_dictionary.get(
        key,
        translations_dictionary.get('start'))
    return command


def read_object(object):
    # zpl_code = ""
    # for method in function_handler:
    #     zpl_code += method(object)
    # print(object.items())
    r = [function_handler2.get(key, function_handler2.get('default'))(value)
         for key, value in object.items()]
    # results = [value(object) for value in function_handler]
    # print(results)
    zpl_code = "".join(r)

    return zpl_code


def read_item(key, value):
    command = translations_dictionary.get(key)
    config_value = "^%s%s" % (command, value)
    return config_value


def get_config_info(config):
    # print('CONFIG')
    # config = object.get('config')
    # zpl_code = read_config(config) if config else ""
    # print(config.values())
    parameters = config.get('parameters')
    zpl_code = (",".join(parameters.values()) if parameters
                else "".join(read_item(key, value)
                             for key, value in config.items()))

    return zpl_code


# def read_config(config):
#     parameters = config.get('parameters')
#     zpl_code = ",".join(parameters.values()) if parameters else ""
#     config_list = ([read_item(key, value) for key, value
#                     in config.items() if key != 'parameters'])
#     zpl_code += "".join(config_list)
#
#     return zpl_code


def get_elements_info(elements):
    # print('ELEMENTS')
    # elements = object.get('elements')
    print(elements)
    if elements:
        zpl_code = "".join([read_object(element) for element in elements])
    else:
        content = object.get('content')
        zpl_code = "%s^FS" % content

    return zpl_code

# function_handler = [
#     lambda object: get_type_info(object),
#     lambda object: get_config_info(object),
#     lambda object: get_elements_info(object)
# ]


# def get_type_info(object):
#     # print('TYPE')
#     type = object.get('type')
#     zpl_code = get_command(type)
#     return zpl_code
