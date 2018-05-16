from .base_label import BaseLabel


class GiftboxLabel(BaseLabel):

    def __init__(self, label_info):
        tag_info = label_info.get('tagInfo')
        self.serial_number = label_info.get('serialNumber')
        self.product = tag_info.get('productName')
        self.color = tag_info.get('productColor')
        self.imei_1 = label_info.get('imei1')
        self.imei_2 = label_info.get('imei2')
        self.bq_ean_piece_1 = tag_info.get('eanBq')[0]
        self.bq_ean_piece_2 = tag_info.get('eanBq')[1:7]
        self.bq_ean_piece_3 = tag_info.get('eanBq')[7:]
        self.bq_ean_barcode = tag_info.get('eanBq')
        self.customer_ean_barcode = tag_info.get('customerIdValue')
        if self.customer_ean_barcode:
            self.customer_ean_piece_1 = self.get('customer_ean_barcode')[0:1]
            self.customer_ean_piece_2 = self.get('customer_ean_barcode')[1:6]
            self.customer_ean_piece_3 = self.get('customer_ean_barcode')[7:-1]
        self.customer_name = tag_info.get('customerName') if self.customer_ean_barcode else ''

        charger_info = tag_info.get('chargerInfo').split('<enter>') if tag_info.get('chargerInfo') else ''
        if charger_info:
            self.charger_info_line_1 = charger_info[0]
            self.charger_info_line_2 = charger_info[1]

        self.additional_info = tag_info.get('additionalInfo')
        free_memory_info = tag_info.get('freeMemory').split('<enter>') if tag_info.get('freeMemory') else ''
        if (free_memory_info):
            self.free_memory_line_1 = free_memory_info[0]
            self.free_memory_line_2 = free_memory_info[1]
            self.free_memory_line_3 = free_memory_info[2]

        # Conditions
        self.free_memory = bool(free_memory_info)
        self.free_memory_lines = len(free_memory_info)
        self.customer = bool(tag_info.get('customerIdType'))
        self.show_charger_info = bool(tag_info.get('chargerInfo'))
        self.charger_info_lines = len(charger_info)
        self.show_imei_1 = bool(tag_info.get('imeisConfig')[0])
        self.show_imei_1_barcode = bool(tag_info.get('imeisConfig')[1])
        self.show_imei_2 = bool(tag_info.get('imeisConfig')[2])
