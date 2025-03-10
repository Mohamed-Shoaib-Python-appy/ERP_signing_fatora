import base64
import frappe
import json

import requests
from zatca.utils import util
from zatca.utils.zatca_connector import get_payload, handle_response

from signing_fatora.api.signer import einvoice_signer
from signing_fatora.api.simplified_invoice_xml_generator import SimplifiedInvoiceXmlGenerator
from signing_fatora.api.utilis import api_helper
from lxml import etree


@frappe.whitelist()
def get_device_data(device_csid, token_data):
    res_binary_token = api_helper.get_binary_tokens(device_csid, token_data)
    print('res_binary_token: ', res_binary_token)
    json_decoded_response = json.loads(res_binary_token) 
    return json_decoded_response


@frappe.whitelist()
def generate_and_sign_invoice(prod_token, private_key, invoice_no):
    SIMG = SimplifiedInvoiceXmlGenerator()
    invoice = frappe.get_doc("Sales Invoice", invoice_no)
    doc = frappe.get_value("ZatcaDocument", {"invoice_no": invoice_no}, "name")
    if not doc:
        frappe.throw(f"لم يتم العثور على مستند ZatcaDocument للفاتورة {invoice_no}")
    doc = frappe.get_doc("ZatcaDocument", doc)

    device = util.get_zatca_device()
    seller = frappe.get_doc("Company", invoice.company)
    buyer = frappe.get_doc(
        "Customer", invoice.customer) if invoice.customer else None
    prev_zatca_doc = util.get_prev_zatca_doc()
    util.update_zatca_doc(
        doc,
        invoice,
        device,
        buyer,
        seller,
        prev_zatca_doc,
    )
    # doc.save()


    payload = get_payload(invoice, doc, None)
    payload_dec = json.loads(json.dumps(payload, cls=util.DateEncoder))
    print("payload_dec: ", payload_dec)
    xml = SIMG.generate(payload_dec)
    xml = xml.encode('utf-8')
    xml_tree = etree.fromstring(xml)
    x509_certificate_content = base64.b64decode(prod_token).decode('utf-8')
    json_payload = einvoice_signer.get_request_api(xml_tree, x509_certificate_content, private_key)
    json_load = json.loads(json_payload)
    print('json_load: ', json_load)
    return json_load


@frappe.whitelist()
def get_invoice_report(device_csid, token_data, invoice_no):
    invoice = frappe.get_doc("Sales Invoice", invoice_no)
    doc = frappe.get_value("ZatcaDocument", {"invoice_no": invoice_no}, "name")
    if not doc:
        frappe.throw(f"لم يتم العثور على مستند ZatcaDocument للفاتورة {invoice_no}")
    doc = frappe.get_doc("ZatcaDocument", doc)
    device = util.get_zatca_device()
    seller = frappe.get_doc("Company", invoice.company)
    buyer = frappe.get_doc(
        "Customer", invoice.customer) if invoice.customer else None
    prev_zatca_doc = util.get_prev_zatca_doc()
    util.update_zatca_doc(
        doc,
        invoice,
        device,
        buyer,
        seller,
        prev_zatca_doc,
    )
    doc.save()
    payload = get_payload(invoice, doc, None)
    # payload_dec = json.dumps(payload, cls=util.DateEncoder)
    # print("payload_dec: ", payload_dec)
    # res = api_helper.report_invoice(device_csid, token_data, payload_dec)
    REPORTING_URL = f"https://saasportal.alfatoora.net/v1/Invoice/Report?deviceID={device_csid}&skipPortalValidation={False}"
    headers = {
        "Authorization": f"Bearer {token_data}",
        "Content-Type": "application/json-patch+json",
    }
    response = requests.post(
        url=REPORTING_URL,
        data=json.dumps(payload, cls=util.DateEncoder),
        headers=headers,
    )
    try:
        response_json = response.json()
    except:
        frappe.throw(
            f"Error: An exception happened. Please ensure the device token is correct - حدث خطأ: يرجى التأكد من صحة رمز الجهاز.")
    print('response_json =', response_json)
    # util.save_json_to_file(response_json, "response_payload.json")

    return handle_response(invoice, doc, response_json, payload, clearance=False, incrementor_test=None)


@frappe.whitelist()
def generate_invoice_qr(invoice_no):
    doc = frappe.get_doc("Sales Invoice", invoice_no)
    if hasattr(doc, "get_qr_code"):
        qr_code = doc.get_qr_code()
        return qr_code
    return None
