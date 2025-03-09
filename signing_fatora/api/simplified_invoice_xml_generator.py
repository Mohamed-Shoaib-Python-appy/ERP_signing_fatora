# import xml.etree.ElementTree as ET
import frappe
from lxml import etree as ET

from signing_fatora.api.xpath import XPaths


class Money:
    def __init__(self, amount, currency_code):
        self.amount = amount
        self.currency_code = currency_code

    def get_amount_string(self, round=True):
        if isinstance(self.amount, dict):
            amount = self.amount.get("Amount", 0)
        else:
            amount = self.amount
        if round:
            return f"{float(amount):.2f}"
        return f"{float(amount)}"


class SimplifiedInvoiceXmlGenerator:
    LINE_ITEM_XML_TEMPLATE = frappe.get_app_path("signing_fatora", "api", "XmlTemplates", "LineItemTemplate.xml")
    SIMPLIFIED_INVOICE_TEMPLATE = frappe.get_app_path("signing_fatora", "api", "XmlTemplates", "SimplifiedInvoiceTemplate.xml")

    def generate(self, invoice):
        xml_string = self.get_file_content(self.SIMPLIFIED_INVOICE_TEMPLATE)
        xml_doc = ET.ElementTree(ET.fromstring(xml_string))
        self.populate_invoice_basic_info(xml_doc, invoice)
        self.populate_supplier_info(xml_doc, invoice)
        self.populate_customer_info(xml_doc, invoice)
        self.populate_discount_info(xml_doc, invoice)
        self.populate_tax_totals(xml_doc, invoice)
        self.populate_invoice_line_items(xml_doc, invoice)
        self.populate_totals(xml_doc, invoice)

        return ET.tostring(xml_doc.getroot(), pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

    def get_file_content(self, file_name):
        # Replace this with actual file reading logic
        with open(file_name, 'r', encoding="utf-8") as file:
            return file.read()

    def populate_totals(self, xml_doc, invoice):
        root = xml_doc.getroot()
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalLineExtensionAmountXpath,
                                      Money(invoice.get('TotalLineNetAmount').get('Amount'), invoice.get('TotalLineNetAmount').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalTaxExclusiveAmountXpath,
                                      Money(invoice.get('TotalAmountWithoutVat').get('Amount'), invoice.get('TotalAmountWithoutVat').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalTaxInclusiveAmountXpath,
                                      Money(invoice.get('TotalAmountWithVat').get('Amount'), invoice.get('TotalAmountWithVat').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalDocLevelDiscountAmountXpath,
                                      Money(invoice.get('TotalDiscountAmount').get('Amount'), invoice.get('TotalDiscountAmount').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalPrepaidAmountXpath,
                                      Money(invoice.get('PrePaidAmount', 0.00), invoice.get('InvoiceCurrencyCode', 'SAR')))
        self.set_currency_node_value(root, XPaths.LegalMonetaryTotalPayableAmountXpath,
                                      Money(invoice.get('TotalAmountWithVat').get('Amount'), invoice.get('TotalAmountWithVat').get('CurrencyCode')))
    

    def populate_invoice_line_items(self, xml_doc, invoice):
        root = xml_doc.getroot()
        for item in invoice['LineItems']:
            line_item_xml = self.get_file_content(self.LINE_ITEM_XML_TEMPLATE)
            line_item_doc = ET.ElementTree(ET.fromstring(line_item_xml))
            line_item_root = line_item_doc.getroot()

            self.set_node_value(line_item_root, XPaths.LineItemIdXpath, item['Id'])
            self.set_attribute_value(line_item_root, XPaths.LineItemInvoicedQuantityXpath, "unitCode", item.get('InvoicedQuantityUnitOfMeasure'))
            self.set_node_value(line_item_root, XPaths.LineItemInvoicedQuantityXpath, item['LineQuantity'])
            self.set_node_value(line_item_root, XPaths.LineItemStandardItemIdentificationXpath, item.get('LineItemStandardItemIdentification'))
            self.set_node_value(line_item_root, XPaths.LineItemBuyersItemIdentificationXpath, item.get('BuyersItemIdentification', ""))
            self.set_node_value(line_item_root, XPaths.LineItemSellersItemIdentificationXpath, item.get('SellersItemIdentification', ""))
            self.set_currency_node_value(line_item_root, XPaths.LineItemLineExtensionAmountXpath,
                                          Money(item.get('LineNetAmount').get('Amount'), item.get('LineNetAmount').get('CurrencyCode')))
            self.set_currency_node_value(line_item_root, XPaths.LineItemTaxAmountXpath,
                                          Money(item.get('LineVatAmount').get('Amount'), item.get('LineVatAmount').get('CurrencyCode')))
            self.set_currency_node_value(line_item_root, XPaths.LineItemRoundingAmountXpath,
                                          Money(item.get('LineAmountWithVat').get('Amount'), item.get('LineAmountWithVat').get('CurrencyCode')))
            self.set_node_value(line_item_root, XPaths.LineItemNameXpath, item['Description'])
            self.set_node_value(line_item_root, XPaths.LineItemTaxPercentXpath, item['LineVatRate'])
            self.set_node_value(line_item_root, XPaths.LineItemTaxClassificationIdXpath, item['TaxSchemeId'])
            self.set_node_value(line_item_root, XPaths.LineItemTaxSchemeXpath, item['TaxScheme'])
            self.set_currency_node_value(line_item_root, XPaths.LineItemPriceAmountXpath,
                                          Money(item.get('LinePrice').get('Amount'), item.get('LinePrice').get('CurrencyCode')), False)
            if not item.get('LineDiscountAmount'):
                self.remove_node(line_item_root, XPaths.LineItemAllowanceXpath)
            else:
                self.set_currency_node_value(line_item_root, XPaths.LineItemDiscountAmountXpath,
                                              Money(item.get('LineDiscountAmount').get('Amount'), item.get('LineDiscountAmount').get('CurrencyCode')))
            # print(line_item_root.getchildren())
            root.append(line_item_root.getchildren()[0])

    def populate_tax_totals(self, xml_doc, invoice):
        root = xml_doc.getroot()
        self.set_currency_node_value(root, XPaths.TaxTotalTaxAmountXpath,
                                      Money(invoice.get('TotalVatAmount').get('Amount'), invoice.get('TotalVatAmount').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.TaxTotalTaxAmountSecondTagXpath,
                                      Money(invoice.get('TotalVatAmount').get('Amount'), invoice.get('TotalVatAmount').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.TaxTotalSubTotalTaxableAmountXpath,
                                      Money(invoice.get('TotalAmountWithoutVat').get('Amount'), invoice.get('TotalAmountWithoutVat').get('CurrencyCode')))
        self.set_currency_node_value(root, XPaths.TaxTotalSubTotalTaxAmountXpath,
                                      Money(invoice.get('TotalVatAmount').get('Amount'), invoice.get('TotalVatAmount').get('CurrencyCode')))
        self.set_node_value(root, XPaths.TaxTotalSubTotalTaxCategoryIdTaxAmountXpath, "S")
        self.set_node_value(root, XPaths.TaxTotalSubTotalTaxPercentTaxAmountXpath, "15")

    def populate_discount_info(self, xml_doc, invoice):
        root = xml_doc.getroot()
        if not invoice.get('TotalDiscountAmount'):
            return self.remove_node(root, XPaths.DocumentLevelDiscountXpath)
        else:
            if not invoice.get('TotalDiscountAmount').get('Amount'):
                self.set_currency_node_value(root, XPaths.DocumentLevelDiscountAmountXpath,
                                              Money(invoice.get('TotalDiscountAmount').get('Amount', 0.00), invoice.get('TotalDiscountAmount').get('CurrencyCode')))
            self.set_node_value(root, XPaths.DocumentLevelDiscountTaxCategoryIdXpath, invoice['TaxCategory'])
            self.set_node_value(root, XPaths.DocumentLevelDiscountTaxPercentIdXpath, invoice['TaxPercent'])
            self.set_node_value(root, XPaths.DocumentLevelTaxExemptionReasonXpath, invoice.get('TaxExemptionReason'))
            self.set_node_value(root, XPaths.DocumentLevelTaxExemptionReasonCodeXpath, invoice.get('TaxExemptionReasonCode'))
        if invoice.get('TaxPercent') != '0':
            self.remove_node(root, XPaths.DocumentLevelTaxExemptionReasonXpath)
            self.remove_node(root, XPaths.DocumentLevelTaxExemptionReasonCodeXpath)

    def populate_customer_info(self, xml_doc, invoice):
        root = xml_doc.getroot()
        buyer = invoice.get('Buyer', {})
        if buyer:
            self.set_node_value(root, XPaths.CustomerStreetNameXpath, buyer.get('Address', {}).get('StreetName', ""))
            self.set_node_value(root, XPaths.CustomerBuildingNumberXpath, buyer.get('Address', {}).get('BuildingNumber', ""))
            self.set_node_value(root, XPaths.CustomerPlotIdentificationXpath, buyer.get('Address', {}).get('AdditionalNo', ""))
            self.set_node_value(root, XPaths.CustomerCitySubdivisionNameXpath, buyer.get('Address', {}).get('City', ""))
            self.set_node_value(root, XPaths.CustomerCityNameXpath, buyer.get('Address', {}).get('District', ""))
            self.set_node_value(root, XPaths.CustomerPostalZoneXpath, buyer.get('Address', {}).get('ZipCode', ""))
            self.set_node_value(root, XPaths.CustomerCountrySubEntityXpath, buyer.get('Address', {}).get('State', ""))
            self.set_node_value(root, XPaths.CustomerCountryXpath, buyer.get('Address', {}).get('Country', ""))
            self.set_node_value(root, XPaths.CustomerRegistrationNameXpath, buyer.get('Name', ''))
            self.set_node_value(root, XPaths.CustomerAdditionalIdTypeXpath, buyer.get('AdditionalIdNumber', ''))
            self.set_attribute_value(root, XPaths.CustomerAdditionalIdTypeXpath, "schemeID", buyer.get('AdditionalIdType', ''))
        self.set_node_value(root, XPaths.CustomerTaxSchemeXpath, "VAT")
        if not buyer:
            self.remove_node(root, XPaths.AccountingCustomerParty)
            return
        if not buyer.get('AdditionalIdNumber'):
            self.remove_node(root, XPaths.CustomerNatNodeXpath)

        if not buyer.get('Name'):
            self.remove_node(root, XPaths.CustomerRegistrationNameNodeXpath)

        if buyer.get('Address') is None:
            self.remove_node(root, XPaths.CustomerAddressXpath)

    def populate_supplier_info(self, xml_doc, invoice):
        root = xml_doc.getroot()
        seller = invoice['Seller']
        self.set_node_value(root, XPaths.SupplierStreetNameXpath, seller['Address']['StreetName'])
        self.set_node_value(root, XPaths.SupplierBuildingNumberXpath, seller['Address']['BuildingNumber'])
        self.set_node_value(root, XPaths.SupplierPlotIdentificationXpath, seller['Address']['AdditionalNo'])
        self.set_node_value(root, XPaths.SupplierCitySubdivisionNameXpath, seller['Address']['City'])
        self.set_node_value(root, XPaths.SupplierCityNameXpath, seller['Address']['District'])
        self.set_node_value(root, XPaths.SupplierPostalZoneXpath, seller['Address']['ZipCode'])
        self.set_node_value(root, XPaths.SupplierCountrySubEntityXpath, seller['Address']['State'])
        self.set_node_value(root, XPaths.SupplierCountryXpath, seller['Address']['Country'])
        self.set_node_value(root, XPaths.SupplierRegistrationNameXpath, seller['Name'])
        self.set_node_value(root, XPaths.SupplierPartyTaxSchemeCompanyId, seller['VatNumber'])
        self.set_node_value(root, XPaths.SupplierTaxSchemeXpath, "VAT")
        self.set_node_value(root, XPaths.SupplierAdditionalIdTypeXpath, seller['AdditionalIdNumber'])
        self.set_attribute_value(root, XPaths.SupplierAdditionalIdTypeXpath, "schemeID", seller['AdditionalIdType'])

    def populate_invoice_basic_info(self, xml_doc, invoice):
        root = xml_doc.getroot()
        self.set_node_value(root, XPaths.InvoiceICVXpath, invoice['ICVIncrementalValue'])
        self.set_node_value(root, XPaths.InvoiceIdXpath, invoice['Id'])
        self.set_node_value(root, XPaths.InvoiceUuidXpath, invoice['ReferenceId'])
        self.set_node_value(root, XPaths.InvoiceNoteXpath, invoice['InvoiceNote'])
        self.set_node_value(root, XPaths.InvoiceActualDeliveryDateXpath, invoice['SupplyDate'])
        self.set_node_value(root, XPaths.InvoiceDocumentCurrencyCodeXpath, invoice['InvoiceCurrencyCode'])
        self.set_node_value(root, XPaths.InvoiceTaxCurrencyCodeXpath, invoice['TaxCurrencyCode'])
        self.set_node_value(root, XPaths.InvoiceIssueDateXpath, invoice['IssueDate'])
        self.set_node_value(root, XPaths.InvoiceIssueTimeXpath, invoice['IssueTime'])
        self.set_node_value(root, XPaths.InvoiceTypeCodeXpath, "388")
        if not invoice.get('InvoiceTypeTransactionCode'):
            invoice_type_code = "0200000"
        else:
            if invoice.get('InvoiceTypeTransactionCode').get('NominalInvoice'):
                nominalInvoice = '1'
            else:
                nominalInvoice = '0'
            if invoice.get('InvoiceTypeTransactionCode').get('ExportsInvoice'):
                exportsInvoice = '1'
            else:
                exportsInvoice = '0'
            if invoice.get('InvoiceTypeTransactionCode').get('SummaryInvoice'):
                summaryInvoice = '10'
            else:
                summaryInvoice = '00'
            invoice_type_code = "020{}{}{}".format(nominalInvoice, exportsInvoice, summaryInvoice)
        self.set_attribute_value(root, XPaths.InvoiceTypeCodeXpath, "name", invoice_type_code)
        self.set_node_value(root, XPaths.InvoiceLatestDeliveryDateXpath, invoice['LastestSupplyDate'])
        self.set_node_value(root, XPaths.InvoicePreviousInvoiceHashXpath, invoice['PreviousHash'])
        if not invoice['InvoiceNote']:
            self.remove_node(root, XPaths.InvoiceNoteXpath)

    def set_node_value(self, parent, xpath, value):
        node = parent.xpath(xpath)
        if node:
            node[0].text = str(value)

    def set_attribute_value(self, parent, xpath, attribute_name, value):
        node = parent.xpath(xpath)
        if node and hasattr(node[0], "attrib"):
            for attr_name, attr_value in node[0].attrib.items():
                if attr_name == attribute_name:
                    node[0].attrib[attr_name] = str(value)

    def set_currency_node_value(self, xml_document, xpath, money, round=True):
        currency_id_attribute_name = "currencyID"
        xml_node = xml_document.xpath(xpath)
        if not xml_node or not isinstance(xml_node[0], ET._Element):
            return
        xml_node = xml_node[0]
        if currency_id_attribute_name in xml_node.attrib:
            xml_node.attrib[currency_id_attribute_name] = money.currency_code
        xml_node.text = money.get_amount_string(round)

    def remove_node(self, parent, xpath):
        node = parent.xpath(xpath)
        if node:
            actual_parent = node[0].getparent()
            if actual_parent is not None:
                actual_parent.remove(node[0])