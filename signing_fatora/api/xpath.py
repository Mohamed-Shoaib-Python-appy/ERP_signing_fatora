class XPaths:
    InvoiceICVXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AdditionalDocumentReference' and *[local-name()='ID' and .='ICV']]/*[local-name() = 'UUID']"

    QrCodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AdditionalDocumentReference' and *[local-name()='ID' and .='QR']]/*[local-name() = 'Attachment']/*[local-name() = 'EmbeddedDocumentBinaryObject']"

    InvoicePreviousInvoiceHashXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AdditionalDocumentReference' and *[local-name()='ID' and .='PIH']]/*[local-name() = 'Attachment']/*[local-name() = 'EmbeddedDocumentBinaryObject']"

    HashXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'UBLExtensions']/*[local-name() = 'UBLExtension']/*[local-name() = 'ExtensionContent']/*[local-name() = 'UBLDocumentSignatures']/*[local-name() = 'SignatureInformation']/*[local-name() = 'Signature']/*[local-name() = 'SignedInfo']/*[local-name() = 'Reference' and @Id='invoiceSignedData']/*[local-name() = 'DigestValue']"

    InvoiceIdXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'ID']"

    InvoiceUuidXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'UUID']"

    InvoiceNoteXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'Note']"

    InvoiceActualDeliveryDateXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'Delivery']/*[local-name() = 'ActualDeliveryDate']"

    InvoiceDocumentCurrencyCodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'DocumentCurrencyCode']"

    InvoiceTaxCurrencyCodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxCurrencyCode']"

    InvoiceTypeCodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceTypeCode']"

    InvoiceIssueDateXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'IssueDate']"

    InvoiceIssueTimeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'IssueTime']"

    InvoiceLatestDeliveryDateXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'Delivery']/*[local-name() = 'LatestDeliveryDate']"

    SupplierStreetNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'StreetName']"

    SupplierBuildingNumberXpath =  "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'BuildingNumber']"

    SupplierPlotIdentificationXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'PlotIdentification']"

    SupplierCitySubdivisionNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CitySubdivisionName']"

    SupplierCityNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CityName']"

    SupplierPostalZoneXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'PostalZone']"

    SupplierCountrySubEntityXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CountrySubentity']"

    SupplierCountryXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'Country']/*[local-name() = 'Country']"

    SupplierRegistrationNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PartyLegalEntity']/*[local-name() = 'RegistrationName']"

    SupplierPartyTaxSchemeCompanyId = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PartyTaxScheme']/*[local-name() = 'CompanyID']"

    SupplierAdditionalIdTypeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PartyIdentification']/*[local-name() = 'ID']"

    SupplierTaxSchemeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingSupplierParty']/*[local-name() = 'Party']/*[local-name() = 'PartyTaxScheme']/*[local-name() = 'TaxScheme']/*[local-name() = 'ID']"

    AccountingCustomerParty = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']"

    CustomerStreetNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'StreetName']"

    CustomerBuildingNumberXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'BuildingNumber']"

    CustomerPlotIdentificationXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'PlotIdentification']"

    CustomerCitySubdivisionNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CitySubdivisionName']"

    CustomerCityNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CityName']"

    CustomerPostalZoneXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'PostalZone']"

    CustomerCountrySubEntityXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'CountrySubentity']"

    CustomerCountryXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']/*[local-name() = 'Country']/*[local-name() = 'Country']"

    CustomerAddressXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PostalAddress']"

    CustomerRegistrationNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PartyLegalEntity']/*[local-name() = 'RegistrationName']"

    CustomerRegistrationNameNodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PartyLegalEntity']"

    CustomerAdditionalIdTypeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PartyIdentification']/*[local-name() = 'ID']"

    CustomerNatNodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PartyIdentification']"

    CustomerTaxSchemeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AccountingCustomerParty']/*[local-name() = 'Party']/*[local-name() = 'PartyTaxScheme']/*[local-name() = 'TaxScheme']/*[local-name() = 'ID']"

    DocumentLevelDiscountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AllowanceCharge']"

    DocumentLevelDiscountAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AllowanceCharge']/*[local-name() = 'Amount']"

    DocumentLevelDiscountTaxCategoryIdXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AllowanceCharge']/*[local-name() = 'TaxCategory']/*[local-name() = 'ID']"

    DocumentLevelDiscountTaxPercentIdXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'AllowanceCharge']/*[local-name() = 'TaxCategory']/*[local-name() = 'Percent']"
    
    TaxTotalTaxAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxAmount']"

    TaxTotalTaxAmountSecondTagXpath =  "(/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxAmount'])[2]"

    TaxTotalSubTotalTaxableAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxableAmount']"

    TaxTotalSubTotalTaxAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxAmount']"

    TaxTotalSubTotalTaxCategoryIdTaxAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxCategory']/*[local-name() = 'ID']"

    TaxTotalSubTotalTaxPercentTaxAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxCategory']/*[local-name() = 'Percent']"

    DocumentLevelTaxExemptionReasonCodeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxCategory']/*[local-name() = 'TaxExemptionReasonCode']"

    DocumentLevelTaxExemptionReasonXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxSubtotal']/*[local-name() = 'TaxCategory']/*[local-name() = 'TaxExemptionReason']"

    CurrencyIdAttributeName = "currencyID"
    
    LineItemXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']"

    LineItemIdXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'ID']"

    LineItemInvoicedQuantityXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'InvoicedQuantity']"

    LineItemLineExtensionAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'LineExtensionAmount']"

    LineItemTaxAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'TaxTotal']/*[local-name() = 'TaxAmount']"

    LineItemRoundingAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'TaxTotal']/*[local-name() = 'RoundingAmount']"

    LineItemNameXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'Name']"

    LineItemStandardItemIdentificationXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'StandardItemIdentification']/*[local-name() = 'ID']"

    LineItemBuyersItemIdentificationXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'BuyersItemIdentification']/*[local-name() = 'ID']"

    LineItemSellersItemIdentificationXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'SellersItemIdentification']/*[local-name() = 'ID']"

    LineItemTaxClassificationIdXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'ClassifiedTaxCategory']/*[local-name() = 'ID']"

    LineItemTaxPercentXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'ClassifiedTaxCategory']/*[local-name() = 'Percent']"

    LineItemTaxSchemeXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Item']/*[local-name() = 'ClassifiedTaxCategory']/*[local-name() = 'TaxScheme']/*[local-name() = 'ID']"

    LineItemPriceAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'Price']/*[local-name() = 'PriceAmount']"

    LineItemAllowanceXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'AllowanceCharge']"

    LineItemDiscountAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'InvoiceLine']/*[local-name() = 'AllowanceCharge']/*[local-name() = 'Amount']"

    LegalMonetaryTotalLineExtensionAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'LineExtensionAmount']"

    LegalMonetaryTotalTaxExclusiveAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'TaxExclusiveAmount']"

    LegalMonetaryTotalTaxInclusiveAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'TaxInclusiveAmount']"

    LegalMonetaryTotalDocLevelDiscountAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'AllowanceTotalAmount']"

    LegalMonetaryTotalPrepaidAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'PrepaidAmount']"

    LegalMonetaryTotalPayableAmountXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'LegalMonetaryTotal']/*[local-name() = 'PayableAmount']"

    InvoiceReferenceXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'BillingReference']/*[local-name() = 'InvoiceDocumentReference']/*[local-name() = 'ID']"

    AdjustmentReasonXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'PaymentMeans']/*[local-name() = 'InstructionNote']"

    SignatureXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'UBLExtensions']/*[local-name() = 'UBLExtension']/*[local-name() = 'ExtensionContent']/*[local-name() = 'UBLDocumentSignatures']/*[local-name() = 'SignatureInformation']/*[local-name() = 'Signature']/*[local-name() = 'SignatureValue']"

    CertificateXpath = "/*[local-name() = 'Invoice']/*[local-name() = 'UBLExtensions']/*[local-name() = 'UBLExtension']/*[local-name() = 'ExtensionContent']/*[local-name() = 'UBLDocumentSignatures']/*[local-name() = 'SignatureInformation']/*[local-name() = 'Signature']/*[local-name() = 'KeyInfo']/*[local-name() = 'X509Data']/*[local-name() = 'X509Certificate']"

    PublickeyHashingXpah = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']//*[local-name()='SignedSignatureProperties']//*[local-name()='SigningCertificate']//*[local-name()='Cert']//*[local-name()='CertDigest']//*[local-name()='DigestValue']"

    SigningTimeXpath = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']//*[local-name()='SignedSignatureProperties']//*[local-name()='SigningTime']"

    IsssuerNameXpath = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='UBLExtension']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='Object']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']//*[local-name()='SignedSignatureProperties']//*[local-name()='SigningCertificate']//*[local-name()='Cert']//*[local-name()='IssuerSerial']//*[local-name()='X509IssuerName']"

    CertificateSerialNumberXpah = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='UBLExtension']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='Object']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']//*[local-name()='SignedSignatureProperties']//*[local-name()='SigningCertificate']//*[local-name()='Cert']//*[local-name()='IssuerSerial']//*[local-name()='X509SerialNumber']"
    
    SignedProperitiesDigestValue = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='SignedInfo']//*[local-name()='Reference'][2]//*[local-name()='DigestValue']"

    SignedCertificateDigestValue = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='UBLExtension']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='Object']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']//*[local-name()='SignedSignatureProperties']//*[local-name()='SigningCertificate']//*[local-name()='Cert']//*[local-name()='CertDigest']//*[local-name()='DigestValue']"

    SignedPropertiesXpath = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']//*[local-name()='ExtensionContent']//*[local-name()='UBLDocumentSignatures']//*[local-name()='SignatureInformation']//*[local-name()='Signature']//*[local-name()='QualifyingProperties']//*[local-name()='SignedProperties']"
