import base64
import hashlib
import json
import os
import re
import tempfile
import frappe
from lxml import etree
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import ec
from OpenSSL import crypto
import qrcode

from signing_fatora.api.utilis import api_helper




class einvoice_signer:

    @staticmethod
    def pretty_print_xml(xml):
        """Pretty prints an XML element."""
        xml_string = etree.tostring(xml, pretty_print=True, encoding='UTF-8').decode('UTF-8')
        return etree.fromstring(xml_string)


    @staticmethod
    def get_request_api(xml, x509_certificate_content, private_key_content):
        """Generates a signed request for an API using the provided XML, X.509 certificate, and private key."""
        resource_paths = {
            "xsl_file": 'Templates/Invoice.xsl',
            "ubl_template": 'Templates/ubl.xml',
            "signature": 'Templates/signature.xml',
            "qr_code": 'Templates/qr.xml'
        }
        resource_paths = {
            "xsl_file": os.path.join(frappe.get_app_path("signing_fatora"), "api", "Templates", "Invoice.xsl"),
            "ubl_template": os.path.join(frappe.get_app_path("signing_fatora"), "api", "Templates", "ubl.xml"),
            "signature": os.path.join(frappe.get_app_path("signing_fatora"), "api", "Templates", "signature.xml"),
            "qr_code": os.path.join(frappe.get_app_path("signing_fatora"), "api", "Templates", "qr.xml"),
        }
        uuid = einvoice_signer.extract_uuid(xml)
        transformed_xml = einvoice_signer.transform_xml(xml, resource_paths["xsl_file"])
        canonical_xml = einvoice_signer.canonicalize_xml(transformed_xml)
        base64_hash = einvoice_signer.generate_base64_hash(canonical_xml)
        return einvoice_signer.sign_simplified_invoice(canonical_xml, base64_hash, x509_certificate_content, private_key_content,
                                                        resource_paths["ubl_template"], resource_paths["signature"], resource_paths["qr_code"], uuid)

    @staticmethod
    def extract_uuid(xml):
        """Extracts the UUID from the given XML document."""
        uuid_nodes = xml.xpath('//cbc:UUID', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'})
        if not uuid_nodes:
            raise Exception("UUID not found in the XML document.")
        return uuid_nodes[0].text


    @staticmethod
    def transform_xml(xml, xsl_file_path):
        """Transforms an XML document using an XSLT stylesheet."""
        xsl = etree.parse(xsl_file_path)
        transform = etree.XSLT(xsl)
        transformed_xml = transform(xml)
        if transformed_xml is None:
            raise Exception("XSL Transformation failed.")
        return transformed_xml


    @staticmethod
    def canonicalize_xml(transformed_xml):
        """ Canonicalizes the given XML element.Canonicalization is the 
        process of converting XML content to a standard format, which is useful 
        for tasks such as digital signatures."""
        return etree.tostring(transformed_xml, method='c14n').decode('utf-8')


    @staticmethod
    def generate_base64_hash(canonical_xml):
        """Generates a base64-encoded SHA-256 hash of the given canonical XML string."""
        hash_bytes = hashlib.sha256(canonical_xml.encode('utf-8')).digest()
        return base64.b64encode(hash_bytes).decode()


    @staticmethod
    def encode_invoice(xml_declaration, canonical_xml):
        """Encodes an XML invoice by combining the XML declaration and canonical XML,
        then encoding the result in base64."""
        updated_xml = f"{xml_declaration}\n{canonical_xml}"
        return base64.b64encode(updated_xml.encode('utf-8')).decode('utf-8')


    @staticmethod
    def sign_simplified_invoice(canonical_xml, base64_hash, x509_certificate_content, private_key_content, ubl_template_path, signature_path, qr_code_path, uuid):
        """Signs a simplified invoice XML document."""
        signature_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        public_key_hashing = einvoice_signer.generate_public_key_hashing(x509_certificate_content)
        pem_certificate = einvoice_signer.wrap_certificate(x509_certificate_content)
        certificate = x509.load_pem_x509_certificate(pem_certificate.encode(), default_backend())
        issuer_name = einvoice_signer.get_issuer_name(certificate)
        serial_number = certificate.serial_number
        signed_properties_hash = einvoice_signer.get_signed_properties_hash(signature_timestamp, public_key_hashing, issuer_name, serial_number)
        signature_value = einvoice_signer.get_digital_signature(base64_hash, private_key_content)
        ubl_content = einvoice_signer.populate_ubl_template(ubl_template_path, base64_hash, signed_properties_hash, signature_value, x509_certificate_content, signature_timestamp, public_key_hashing, issuer_name, serial_number)
        updated_xml_string = einvoice_signer.insert_ubl_into_xml(canonical_xml, ubl_content)

        ecdsa_result = einvoice_signer.get_public_key_and_signature(x509_certificate_content)
        qr_code = api_helper.generate_qr_code(canonical_xml, base64_hash, signature_value, ecdsa_result)
        # qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        # qr.add_data(qr_code)
        # qr.make(fit=True)
        # img = qr.make_image(fill_color="black", back_color="white")
        # img.save("zatka_qr.png")

        updated_xml_string = einvoice_signer.insert_signature_into_xml(updated_xml_string, signature_path, qr_code_path,  qr_code)

        # with open("XmlTemplates/updated_invoice.xml", "w", encoding="utf-8") as file:
        #     file.write(f'<?xml version="1.0" encoding="UTF-8"?>\n{updated_xml_string}')

        base64_invoice = einvoice_signer.encode_invoice('<?xml version="1.0" encoding="UTF-8"?>\n', updated_xml_string)
        return json.dumps({
            "invoiceHash": base64_hash,
            "uuid": uuid,
            "invoice": base64_invoice,
        })


    @staticmethod
    def wrap_certificate(x509_certificate_content):
        """Wraps a given X.509 certificate content into the standard PEM format."""
        return "-----BEGIN CERTIFICATE-----\n" + \
               "\n".join([x509_certificate_content[i:i + 64] for i in range(0, len(x509_certificate_content), 64)]) + \
               "\n-----END CERTIFICATE-----"


    @staticmethod
    def generate_public_key_hashing(x509_certificate_content):
        """Generates a base64-encoded SHA-256 hash of the given X.509 certificate content."""
        hash_bytes = hashlib.sha256(x509_certificate_content.encode('utf-8')).digest()
        hash_hex = hash_bytes.hex()
        return base64.b64encode(hash_hex.encode('utf-8')).decode('utf-8')


    @staticmethod
    def populate_ubl_template(ubl_template_path, base64_hash, signed_properties_hash, signature_value, x509_certificate_content, signature_timestamp, public_key_hashing, issuer_name, serial_number):
        """Populates a UBL template with provided signature and certificate details."""
        with open(ubl_template_path, 'r') as ubl_file:
            ubl_content = ubl_file.read()
            ubl_content = ubl_content.replace("INVOICE_HASH", base64_hash)
            ubl_content = ubl_content.replace("SIGNED_PROPERTIES", signed_properties_hash)
            ubl_content = ubl_content.replace("SIGNATURE_VALUE", signature_value)
            ubl_content = ubl_content.replace("CERTIFICATE_CONTENT", x509_certificate_content)
            ubl_content = ubl_content.replace("SIGNATURE_TIMESTAMP", signature_timestamp)
            ubl_content = ubl_content.replace("PUBLICKEY_HASHING", public_key_hashing)
            ubl_content = ubl_content.replace("ISSUER_NAME", issuer_name)
            ubl_content = ubl_content.replace("SERIAL_NUMBER", str(serial_number))
        return ubl_content


    @staticmethod
    def insert_ubl_into_xml(canonical_xml, ubl_content):
        """Inserts UBL content into a canonical XML string."""
        insert_position = canonical_xml.find('>') + 1
        return canonical_xml[:insert_position] + ubl_content + canonical_xml[insert_position:]
    

    @staticmethod
    def insert_signature_into_xml(updated_xml_string, signature_path, qr_code_path, qr_code):
        """Inserts a digital signature and a QR code into an XML string."""
        with open(signature_path, 'r') as signature_file:
            signature_content = signature_file.read()

        with open(qr_code_path, 'r') as qr_file:
            qr_content = qr_file.read()
            qr_content = qr_content.replace("BASE64_QRCODE", qr_code)

        insert_position_signature = updated_xml_string.find('<cac:AccountingSupplierParty>')
        if insert_position_signature != -1:
            return updated_xml_string[:insert_position_signature] + qr_content + signature_content + updated_xml_string[insert_position_signature:]
        else:
            raise Exception("The <cac:AccountingSupplierParty> tag was not found in the XML.")


    @staticmethod
    def get_issuer_name(certificate):
        """Extracts and formats the issuer name from a given certificate."""
        issuer = certificate.issuer
        issuer_name_parts = []

        issuer_dict = {}
        for attr in issuer:
            key = attr.oid._name
            if key in issuer_dict:
                if isinstance(issuer_dict[key], list):
                    issuer_dict[key].append(attr.value)
                else:
                    issuer_dict[key] = [issuer_dict[key], attr.value]
            else:
                issuer_dict[key] = attr.value

        if 'commonName' in issuer_dict:
            issuer_name_parts.append(f"CN={issuer_dict['commonName']}")

        if 'domainComponent' in issuer_dict:
            dc_list = issuer_dict['domainComponent']
            if isinstance(dc_list, list):
                dc_list.reverse()
                for dc in dc_list:
                    if dc:
                        issuer_name_parts.append(f"DC={dc}")

        return ", ".join(issuer_name_parts)


    @staticmethod
    def get_signed_properties_hash(signing_time, digest_value, x509_issuer_name, x509_serial_number):
        """Generates a base64-encoded SHA-256 hash of the signed properties XML string."""
        # Construct the XML string with exactly 36 spaces in front of <xades:SignedSignatureProperties>
        xml_string = (
            '<xades:SignedProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Id="xadesSignedProperties">\n'
            '                                    <xades:SignedSignatureProperties>\n'
            '                                        <xades:SigningTime>{}</xades:SigningTime>\n'.format(signing_time) +
            '                                        <xades:SigningCertificate>\n'
            '                                            <xades:Cert>\n'
            '                                                <xades:CertDigest>\n'
            '                                                    <ds:DigestMethod xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>\n'
            '                                                    <ds:DigestValue xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{}</ds:DigestValue>\n'.format(digest_value) +
            '                                                </xades:CertDigest>\n'
            '                                                <xades:IssuerSerial>\n'
            '                                                    <ds:X509IssuerName xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{}</ds:X509IssuerName>\n'.format(x509_issuer_name) +
            '                                                    <ds:X509SerialNumber xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{}</ds:X509SerialNumber>\n'.format(x509_serial_number) +
            '                                                </xades:IssuerSerial>\n'
            '                                            </xades:Cert>\n'
            '                                        </xades:SigningCertificate>\n'
            '                                    </xades:SignedSignatureProperties>\n'
            '                                </xades:SignedProperties>'
        )

        xml_string = xml_string.replace("\r\n", "\n").strip()
        hash_bytes = hashlib.sha256(xml_string.encode('utf-8')).digest()
        hash_hex = hash_bytes.hex()
        return base64.b64encode(hash_hex.encode('utf-8')).decode('utf-8')


    @staticmethod
    def get_digital_signature(xml_hashing, private_key_content):
        """Generates a digital signature for the given XML hash using the provided private key."""
        try:
            hash_bytes = base64.b64decode(xml_hashing)
            if not hash_bytes:
                raise Exception("Failed to decode the base64-encoded XML hashing.")
            
            private_key_content = private_key_content.strip()
            if "-----BEGIN EC PRIVATE KEY-----" not in private_key_content and "-----END EC PRIVATE KEY-----" not in private_key_content:
                private_key_content = f"-----BEGIN EC PRIVATE KEY-----\n{private_key_content}\n-----END EC PRIVATE KEY-----"

            private_key = load_pem_private_key(private_key_content.encode(), password=None)
            if not private_key:
                raise Exception("Failed to load private key.")

            signature = private_key.sign(
                hash_bytes,
                ec.ECDSA(hashes.SHA256())
            )
            return base64.b64encode(signature).decode()
        except Exception as e:
            raise Exception(f"Failed to process signature: {e}")
    
    @staticmethod
    def get_public_key_and_signature(certificate_base64):
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.pem') as temp_file:
                cert_content = "-----BEGIN CERTIFICATE-----\n"
                cert_content += "\n".join([certificate_base64[i:i+64] for i in range(0, len(certificate_base64), 64)])
                cert_content += "\n-----END CERTIFICATE-----\n"
                temp_file.write(cert_content)
                temp_file_path = temp_file.name

            with open(temp_file_path, 'r') as f:
                cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

            pub_key = crypto.dump_publickey(crypto.FILETYPE_ASN1, cert.get_pubkey())
            pub_key_details = crypto.load_publickey(crypto.FILETYPE_ASN1, pub_key).to_cryptography_key().public_numbers()

            x = pub_key_details.x.to_bytes(32, byteorder='big').rjust(32, b'\0')
            y = pub_key_details.y.to_bytes(32, byteorder='big').rjust(32, b'\0')

            public_key_der = b'\x30\x56\x30\x10\x06\x07\x2A\x86\x48\xCE\x3D\x02\x01\x06\x05\x2B\x81\x04\x00\x0A\x03\x42\x00\x04' + x + y

            cert_pem = open(temp_file_path, 'r').read()
            matches = re.search(r'-----BEGIN CERTIFICATE-----(.+)-----END CERTIFICATE-----', cert_pem, re.DOTALL)
            if not matches:
                raise Exception("Error extracting DER data from certificate.")
            
            der_data = base64.b64decode(matches.group(1).replace('\n', ''))
            sequence_pos = der_data.rfind(b'\x30', -72)
            signature = der_data[sequence_pos:]

            return {
                'public_key': public_key_der,
                'signature': signature
            }
        except Exception as e:
            raise Exception("[Error] Failed to process certificate: " + str(e))
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
