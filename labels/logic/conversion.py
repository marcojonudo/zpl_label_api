translations_dictionary = {
    "GIFTBOX": "XA",
    "coordinates_origin": "LH",
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
        }
        # {
        #     "type": "image",
        #     "config": [
        #         {
        #             "type": "position",
        #             "content": "20,200"
        #         }
        #     ],
        #     "content": "LABORATORY_GIFTBOX_X"
        # }
    ]
}


def get_command(key):
    command = "^%s" % translations_dictionary.get(key)
    return command


def read_item(key, value):
    command = translations_dictionary.get(key)
    config_value = "^%s%s" % (command, value)
    return config_value


def read_config(config):
    parameters = config.get('parameters')
    zpl_code = ",".join(list(parameters.values())) if parameters else ""
    config_list = ([read_item(key, value) for key, value
                    in config.items() if key != 'parameters'])
    zpl_code += "".join(config_list)

    return zpl_code


def close_label(zpl_code):
    return "%s^XZ" % zpl_code


function_handler = {
    'type': lambda object: get_type_info(object),
    'config': lambda object: get_config_info(object),
    'elements': lambda object: get_elements_info(object)
}


def get_type_info(object):
    type = object.get('type')
    zpl_code = get_command(type)
    return zpl_code


def get_config_info(object):
    config = object.get('config')
    zpl_code = read_config(config) if config else ""
    return zpl_code


def get_elements_info(object):
    elements = object.get('elements')
    if elements:
        zpl_code = "".join([read_object(element) for element in elements])
    else:
        content = object.get('content')
        zpl_code = "%s^FS" % content

    return zpl_code


def read_object(object):
    results = [value(object) for value in function_handler.values()]
    zpl_code = "".join(results)
    # type = object.get('type')
    # zpl_code = get_command(type)
    #
    # config = object.get('config')
    # zpl_code += read_config(config) if config else ""
    #
    # elements = object.get('elements')
    # if elements:
    #     zpl_code += "".join([read_object(element) for element in elements])
    # else:
    #     content = object.get('content')
    #     zpl_code += "%s^FS" % content

    return zpl_code


def test():
    # 1. Generar configuracion
    label = read_object(label_json)
    label = close_label(label)
    # 2. Generar contenido
    print(label)
    return label
