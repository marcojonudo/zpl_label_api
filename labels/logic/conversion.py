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
    "config": [
        {
            "type": "coordinates_origin",
            "content": "0,0"
        },
        {
            "type": "encoding",
            "content": "28"
        }
    ],
    "elements": [
        {
            "type": "block",
            "config": [
                # {
                #     "width": "250"
                # },
                {
                    "type": "position",
                    "content": "20,50"
                }
            ],
            "elements": [
                {
                    "type": "text",
                    "content": "Texto de prueba"
                }
            ]
        },
        {
            "type": "block",
            "config": [
                {
                    "type": "position",
                    "content": "20,80"
                }
            ],
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


def get_command(object, text):
    command_text = object.get(text)
    command = "^%s" % translations_dictionary.get(command_text)
    return command


def close_label(zpl_code):
    return "%s^XZ" % zpl_code


def read_object(object):
    zpl_code = get_command(object, 'type')
    configs = object.get('config')
    if (configs):
        for config in configs:
            command = get_command(config, 'type')
            config_content = config.get('content')
            zpl_code += "%s%s" % (command, config_content)

    elements = object.get('elements')
    if elements:
        for element in elements:
            zpl_code += read_object(element)
    else:
        content = object.get('content')
        zpl_code += "%s^FS" % content

    return zpl_code


def test():
    # 1. Generar configuracion
    label = read_object(label_json)
    label = close_label(label)
    # 2. Generar contenido
    print(label)
    return label
