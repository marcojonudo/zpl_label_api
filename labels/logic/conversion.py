from bson import CodecOptions, SON
import pprint

translations = None

key_handler = {
    'position': lambda position: "%s%s" % (get_command('position'), position),
    'config': lambda config: get_config_info(config),
    'content': lambda content: get_content_info(content),
    'default': lambda object: get_command(object)
}


conditions = [
    (lambda object, data: object.get('customer') == bool(data.get('customer'))
     and object.get('free_memory') == bool(data.get('free_memory')))
]


def get_label(mongo, label_type):
    """Get ZPL code for given label type and label info."""
    global translations
    labels_collection, translations_collection, elements_collection = get_collections(mongo)
    stored_label, translations, stored_elements = get_db_info(labels_collection, translations_collection, elements_collection, label_type)

    data = {
        'product': 'Aquaris X',
        'color': 'black',
        'serial_number': 'AA123456',
        'free_memory': True,
        'free_memory_lines': 1,
        'customer': True,
        'show_charger_info': True,
        'charger_info_lines': 2
    }

    label_elements_names = stored_label.get('content')

    converted_elements = [get_element(data, stored_elements, element_name) for element_name in label_elements_names]
    converted_elements = [element for element in converted_elements if element]

    stored_label['content'] = converted_elements
    # pprint.pprint(stored_label)
    # pprint.pprint(converted_elements)
    # bq_ean_barcode_condition = (lambda object, data:
    #                             object.get('customer') == bool(data.get('customer'))
    #                             and object.get('free_memory') == bool(data.get('free_memory')))
    #
    # bq_ean_barcode = labels_collection.find_one(
    #     {"type": label_type, "element": "bq_ean_barcode"}
    # )
    # elements = bq_ean_barcode.get('elements')
    # element = ([elem for elem in elements if bq_ean_barcode_condition(elem.get('conditions'), data)])
    # print(element)
    #
    zpl_code = read_object(stored_label)
    zpl_code += get_command('close')

    return zpl_code


def get_element(label_data, stored_elements, element_name):
    print("*******************************")
    print(element_name)
    possible_elements = next(element.get('possible_elements') for element in stored_elements if element.get('element') == element_name)

    chosen_element = next((element for element in possible_elements if check_data(label_data, element)), None)
    element = chosen_element.get('object') if chosen_element else None
    if element:
        element = fill_element(element, label_data.get(element_name))

    return element


def check_data(label_data, element):
    conditions = element.get('conditions')
    match = True
    if conditions:
        # print("----------------------------------")
        not_matched_element = next((value for key, value in conditions.items() if label_data.get(key) != value), None)
        print([value for key, value in conditions.items() if label_data.get(key) == value])
        match = False if not_matched_element else True
        # print("%s | %s" % (not_matched_element, match))
        # for key, value in conditions.items():
        #     match = True if label_data.get(key) == value else False
        print(match)
        # print("++++++++++++++++++++++++++++++++++")

    return match


def fill_element(element, field):
    """Fills element content with the one got from label data."""
    content = element.get('content')
    if isinstance(content, str):
        element['content'] = content if content else field
        return element

    element['content'] = [fill_element(content[0], field)]
    return element


def get_collections(mongo):
    """Get labels and translations collections from mongo."""
    son_options = CodecOptions(document_class=SON)
    labels_collection = mongo.db.labels.with_options(codec_options=son_options)
    translations_collection = mongo.db.translations
    elements_collection = mongo.db.elements.with_options(codec_options=son_options)

    return labels_collection, translations_collection, elements_collection


def get_db_info(labels_collection, translations_collection, elements_collection, label_type):
    stored_label = labels_collection.find_one(
        {'type': label_type}, {'_id': False}
    )
    translations = translations_collection.find_one(
        {'direction': 'text_to_zpl'}
    )
    stored_elements = elements_collection.find(
        {'type': label_type}
    )
    stored_elements = [element for element in stored_elements]

    return stored_label, translations, stored_elements


def read_object(object):
    """Read and translate recursively a JSON object to ZPL.

    Kyeword argument:
    object -- Label entity read from MongoDB

    Return:
    zpl_code -- String containing the translated ZPL code
    """
    zpl_fragments = (key_handler.get(key, key_handler.get('default'))(value)
                     for key, value in object.items() if key != 'element')
    zpl_code = "".join(zpl_fragments)

    return zpl_code


def get_command(key):
    """Get ZPL command for given parameter.

    Keyword argument:
    key -- ZPL command before translating (ej. 'block', 'text', 'image')
    """
    command = "^%s" % translations.get(key, translations.get('start'))
    return command


def read_item(key, value):
    """Translate given key and value to a complete ZPL command.

    Keyword arguments:
    key -- ZPL command before translating
    value -- ZPL command value (ej. position '20,200')
    """
    command = translations.get(key)
    config_value = "^%s%s" % (command, value)
    return config_value


def get_config_info(config):
    """Read and transalte config info to ZPL"""
    parameters = config.get('parameters')
    zpl_code = (",".join(parameters.values()) if parameters
                else "".join(read_item(key, value)
                             for key, value in config.items()))

    return zpl_code


def get_content_info(content):
    """Read content info and translate it to ZPL"""
    if isinstance(content, list):
        zpl_code = "".join(read_object(object) for object in content)
    else:
        zpl_code = "%s^FS" % content

    return zpl_code
