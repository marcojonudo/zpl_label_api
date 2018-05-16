from bson import CodecOptions, SON

translations = None

key_handler = {
    'position': lambda position: "%s%s" % (get_command('position'), position),
    'config': lambda config: get_config_info(config),
    'content': lambda content: get_content_info(content),
    'default': lambda object: get_command(object)
}


def get_label(mongo, label_type, label_info):
    """Get ZPL code for given label type and label info."""
    global translations
    labels_collection, translations_collection, elements_collection = get_collections(mongo)
    stored_label, translations, stored_elements = get_db_info(labels_collection, translations_collection, elements_collection, label_type)

    label_elements_names = stored_label.get('content')

    converted_elements = [get_element(label_info, stored_elements, element_name) for element_name in label_elements_names]
    converted_elements = [element for element in converted_elements if element]

    stored_label['content'] = converted_elements

    zpl_code = read_object(stored_label)
    zpl_code += get_command('close')

    return zpl_code


def get_element(label_info, stored_elements, element_name):
    possible_elements = next(element.get('possible_elements') for element in stored_elements if element.get('element') == element_name)

    chosen_element = next((element for element in possible_elements if check_data(label_info, element)), None)
    element = chosen_element.get('object') if chosen_element else None
    if element and hasattr(label_info, element_name):
        element = fill_element(element, getattr(label_info, element_name))

    return element


def check_data(label_info, element):
    """Checks if given conditions match label data"""
    conditions = element.get('conditions')
    match = True
    if conditions:
        not_matched_element = next((value for key, value in conditions.items() if getattr(label_info, key) != value), None)
        match = False if not_matched_element else True

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
