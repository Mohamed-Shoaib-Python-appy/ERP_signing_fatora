import base64
import json
import time
import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            total_seconds = int(obj.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return super().default(obj)


class api_helper:
    @staticmethod
    def post_request_with_retries(url, headers, json_payload, params=None, auth=None, retries=3, backoff_factor=1):
        """Sends a POST request to the specified URL with retries and exponential backoff."""
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, params=params, data=json_payload, auth=auth)
                if response.status_code != 200:
                    print(f"HTTP error: {response.status_code} - {response.text}")
                    return {"error": f"HTTP error: {response.status_code} - {response.text}"}
                return response.text
            except requests.exceptions.ConnectionError as e:
                print(f"ConnectionError: {e}. Attempt {attempt + 1} of {retries}.")
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise
    
    @staticmethod
    def get_request_with_retries(url, headers, params, retries=3, backoff_factor=1):
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    # raise Exception(f"HTTP error: {response.status_code} - {response.text}")
                    print(f"HTTP error: {response.status_code} - {response.text}")
                    return {"error": f"HTTP error: {response.status_code} - {response.text}"}
                return response.text
            except requests.exceptions.ConnectionError as e:
                print(f"ConnectionError: {e}. Attempt {attempt + 1} of {retries}.")
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise


    @staticmethod
    def get_binary_tokens(deviceId, token, retries=3, backoff_factor=1):
        url = 'https://saasportal.alfatoora.net/v1/Device/GetBinaryTokens'
        params = {
            'deviceId': f'{deviceId}',
        }
        headers = {
            'accept': 'text/plain',
            'Authorization': 'Bearer {}'.format(token),
        }
        return api_helper.get_request_with_retries(url, headers, params, retries=retries, backoff_factor=backoff_factor)
    
    @staticmethod
    def report_invoice(deviceId, token, data, retries=3, backoff_factor=1):
        url = 'https://saasportal.alfatoora.net/v1/Invoice/Report'
        params = {
            'deviceID': f'{deviceId}',
            'skipPortalValidation': 'false',
            'hasExternalSubscription': 'false',
            'isSaveXml': 'false',
            'isSavePayload': 'false',
            'isSaveZatcaResponse': 'false',
        }
        headers = {
            'accept': 'text/plain',
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json-patch+json',
        }
        # data = json.dumps(invoice, cls=DateEncoder)
        return api_helper.post_request_with_retries(url, headers, data, params=params, retries=retries, backoff_factor=backoff_factor)
    
    @staticmethod
    def generate_qr_code(canonical_xml, invoice_hash, signature_value, ecdsa_result):
        invoice_details = api_helper.get_invoice_details(canonical_xml)
        invoice_details.append(invoice_hash)
        invoice_details.append(signature_value)
        invoice_details.append(ecdsa_result['public_key'])
        invoice_details.append(ecdsa_result['signature'])   
        base64_qr_code = api_helper.generate_qr_code_from_values(invoice_details)
        return base64_qr_code
    
    @staticmethod
    def get_invoice_details(xml):
        xml_object = ET.fromstring(xml)

        invoice_type_code_name = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoiceTypeCode').get('name')
        supplier_name = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName').text
        company_id = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID').text
        issue_date_time = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate').text + 'T' + xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueTime').text
        payable_amount = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}LegalMonetaryTotal/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PayableAmount').text
        tax_amount = xml_object.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxAmount').text

        return [
            invoice_type_code_name,
            supplier_name,
            company_id,
            issue_date_time,
            payable_amount,
            tax_amount
        ]
    
    @staticmethod
    def generate_qr_code_from_values(invoice_details):
        data = b''  
        for key, value in enumerate(invoice_details[1:], start=1):
            if isinstance(value, str):
                value = value.encode('utf-8')
            
            tlv_data = api_helper.write_tlv(key, value)
            data += tlv_data
        if not data:
            print("No data generated for QR code!")
        
        return base64.b64encode(data).decode()
    
    @staticmethod
    def write_tlv(tag, value):
        if value is None:
            raise ValueError("Please provide a value!")
        tlv = api_helper.write_tag(tag)
        length = len(value)
        tlv += api_helper.write_length(length)
        tlv += value
        return tlv
    
    @staticmethod
    def write_length(length):
        if length <= 0x7F:
            return bytes([length])
        length_bytes = []
        while length > 0:
            length_bytes.insert(0, length & 0xFF)
            length >>= 8
        return bytes([0x80 | len(length_bytes)]) + bytes(length_bytes)
    
    @staticmethod
    def write_tag(tag):
        result = bytes()
        flag = True
        for i in range(3, -1, -1):
            num = (tag >> (8 * i)) & 0xFF
            if num != 0 or not flag or i == 0:
                if flag and i != 0 and (num & 0x1F) != 0x1F:
                    raise ValueError(f"Invalid tag value: {tag}")
                result += bytes([num])
                flag = False
        return result