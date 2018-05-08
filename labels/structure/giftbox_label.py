import BaseLabel


class GiftboxLabel(BaseLabel):

    serialNumber = ''
    product = ''
    colour = ''
    imei1 = ''
    imei2 = ''
    imeisConfig = ''
    eanBq = ''
    eanOutlet = ''
    eanCustomer = ''
    sku = ''
    customerName = ''
    chargerInfo = ''
    additionalInfo = ''
    additionalInfoCode = ''
    freeMemory = ''
    showCountriesTable = False
    bigSerialNumberBarcode = False

    def __init__(self, label_info):
        self.test = label_info
