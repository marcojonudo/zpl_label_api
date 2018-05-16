# from .giftbox_label import GiftboxLabel


class BaseLabel:

    product = ''
    color = ''
    serial_number = ''
    serial_number_barcode = None
    imei_1 = ''
    imei_1_barcode = None
    imei_2 = ''
    imeis_config = ''
    free_memory_line_1 = ''
    free_memory_line_2 = ''
    free_memory_line_3 = ''
    bq_ean_barcode = ''
    bq_ean_piece_1 = ''
    bq_ean_piece_2 = ''
    bq_ean_piece_3 = ''
    outlet_ean = ''
    customer_ean_piece_1 = ''
    customer_ean_piece_2 = ''
    customer_ean_piece_3 = ''
    customer_ean_barcode = ''
    customer_name = ''
    charger_info_line_1 = ''
    charger_info_line_2 = ''
    additional_info = ''

    # Conditions
    show_imei_1 = False
    show_imei_1_barcode = False
    show_imei_2 = False
    free_memory_lines = 0
    customer = False
    free_memory = False
    free_memory_lines = 0
    show_charger_info = False
    charger_info_lines = 0
    show_countries_table = False

    # label_types = {
    # 'giftbox': lambda: GiftboxLabel()
    # }

    def __init__(self):
        print('hola')

    def get_label(self, type, label_info):
        label = self.label_types.get(type)
        return label
