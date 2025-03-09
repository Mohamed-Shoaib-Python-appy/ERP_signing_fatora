// Copyright (c) 2025, leomedo and contributors
// For license information, please see license.txt


frappe.ui.form.on('signing', {
    refresh: function(frm) {
        
        frm.fields_dict['signing_response'].wrapper.style.overflow = 'auto';
        // frm.fields_dict['signing_response'].wrapper.style.whiteSpace = 'nowrap';
		frm.fields_dict['signing_response'].wrapper.style.maxHeight = '300px';
        frm.fields_dict['signing_response'].wrapper.style.marginBottom = '15px';

        frm.fields_dict['reporting_response'].wrapper.style.overflow = 'auto';
        frm.fields_dict['reporting_response'].wrapper.style.maxHeight = '300px';
        frm.fields_dict['reporting_response'].wrapper.style.marginBottom = '15px';

        frm.toggle_display('prod_binary_token', true);
        frm.toggle_display('prod_secret', true);
        frm.toggle_display('private_key', true);
        frm.toggle_display('signing_response', true);
        if (frm.doc.signing_response) {
            frm.toggle_display('custom_download_xml', true);
        }
        frm.toggle_display('reporting_response', true);
        if (frm.doc.reporting_response) {
            frm.toggle_display('xml', true);
        }
        // if (frm.doc.reporting_response) {
        //     frm.toggle_display('qr', true);
        // }
        if (frm.doc.custom_qr_code_html) {
            frm.toggle_display('custom_qr_code_html', true);
        }
    }});
    

frappe.ui.form.on("signing", "get_token", function (frm) {
    let device_number = frm.doc.device_number
    if (!device_number) {
        frappe.msgprint(__('Please enter a device number'));
        return;
    }
    // Get device
    const now = frappe.datetime.now_datetime()
    frappe.db.get_doc('ZatcaDevice', device_number)
    .then(device => {
        // console.log('device =', device);
        console.log('device.device_csid =', device.device_csid);
        console.log('device.token_data =', device.token_data);
        frappe.call({
            method: 'signing_fatora.api.api.get_device_data',
            args: { device_csid: device.device_csid, token_data: device.token_data, now: now },
            callback: function(response) {
                console.log('response =', response);
                frm.set_value('prod_binary_token', response.message.prodBinaryToken);
                frm.set_value('prod_secret', response.message.prodSecret);
                frm.set_value('private_key', response.message.privateKey);
                frm.toggle_display('prod_binary_token', true);
                frm.toggle_display('prod_secret', true);
                frm.toggle_display('private_key', true);
                frm.save();
            }
        });
    });

    });

frappe.ui.form.on("signing", "sign", function (frm) {
    let invoice_number = frm.doc.invoice_number
    let prod_binary_token = frm.doc.prod_binary_token
    let private_key = frm.doc.private_key
    if (!invoice_number) {
        frappe.msgprint(__('Please enter the invoice number'));
        return;
    }
    if (!prod_binary_token) {
        frappe.msgprint(__('Please get the token first'));
        return;
    }
    if (!private_key) {
        frappe.msgprint(__('Please get the token first'));
        return;
    }

    frappe.call({
        method: 'signing_fatora.api.api.generate_and_sign_invoice',
        args: { prod_token: prod_binary_token, private_key: private_key, invoice_no: invoice_number},
        callback: function(response) {
            console.log('response =', response.message);
            frm.set_value('signing_response', JSON.stringify(response.message));
            frm.toggle_display('signing_response', true);
            frm.toggle_display('custom_download_xml', true);
            frm.save();
        }
    });
    
});

frappe.ui.form.on("signing", "custom_download_xml", function (frm) {
    let data_dict = JSON.parse(frm.doc.signing_response || "{}");
    // console.log('data_dict =', data_dict);

    if (!data_dict) {
        frappe.msgprint(__('Please sign the invoice first'));
        return;
    }
    
    try {
        let base64Data = data_dict.invoice;
        let xmlContent = atob(base64Data);
        let blob = new Blob([xmlContent], { type: 'application/xml' });

        // إنشاء رابط تحميل الملف
        let link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        let fileName = frm.doc.invoice_number ? `${frm.doc.invoice_number}.xml` : 'document.xml';
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        frappe.msgprint(__('Error decoding the XML file.'));
        console.error('Decoding Error:', error);
    }
    
});

frappe.ui.form.on("signing", "report", function (frm) {
    let invoice_number = frm.doc.invoice_number
    let device_number = frm.doc.device_number

    if (!invoice_number) {
        frappe.msgprint(__('Please enter the invoice number'));
        return;
    }
    if (!device_number) {
        frappe.msgprint(__('Please enter a device number'));
        return;
    }

    frappe.db.get_doc('ZatcaDevice', device_number)
        .then(device => {
            // console.log('device =', device);
            // console.log('device.device_csid =', device.device_csid);
            // console.log('device.token_data =', device.token_data);
            frappe.call({
                method: 'signing_fatora.api.api.get_invoice_report',
                args: { device_csid: device.device_csid, token_data: device.token_data, invoice_no: invoice_number},
                callback: function(response) {
                    console.log('response =', response.message);
                    frm.set_value('reporting_response', JSON.stringify(response.message));
                    // frm.set_value('reporting_response', response.message);
                    frm.toggle_display('reporting_response', true);
                    frm.toggle_display('xml', true);
                    frm.toggle_display('qr', true);
                    frm.save();
                }
            });
        });   

});

frappe.ui.form.on("signing", "xml", function (frm) {
    let data_dict = JSON.parse(frm.doc.reporting_response || "{}");
    // console.log('data_dict =', data_dict);
    if (!data_dict) {
        frappe.msgprint(__('Please report the invoice first'));
        return;
    }

    // try {
    //     let base64Data = data_dict.xml;
    //     let xmlContent = atob(base64Data);
    //     let blob = new Blob([xmlContent], { type: 'application/xml' });

    //     // إنشاء رابط تحميل الملف
    //     let link = document.createElement('a');
    //     link.href = URL.createObjectURL(blob);
    //     let fileName = frm.doc.invoice_number ? `${frm.doc.invoice_number}.xml` : 'document.xml';
    //     link.download = fileName;
    //     document.body.appendChild(link);
    //     link.click();
    //     document.body.removeChild(link);
    // } catch (error) {
    //     frappe.msgprint(__('Error decoding the XML file.'));
    //     console.error('Decoding Error:', error);
    // }
    window.open(
        "/api/method/zatca.utils.util.download_xml_file?invoice_no=" +
        frm.doc.invoice_number +
        "&invoice_type=Sales Invoice",
        "_blank"
    );

});

frappe.ui.form.on("signing", "qr", function (frm) {
    let data_dict = JSON.parse(frm.doc.reporting_response || "{}");
    // console.log('data_dict =', data_dict);
    if (!data_dict) {
        frappe.msgprint(__('Please report the invoice first'));
        return;
    }

    if (data_dict.generatedQR) {
        // console.log('data_dict.generatedQR =', data_dict.generatedQR);
        // إنشاء عنصر HTML لعرض الـ QR
        let qr_div = $('<div id="qrcode" style="padding: 10px; background: white; display: inline-block;"></div>').appendTo(frm.fields_dict.custom_qr_code_html.wrapper);

        // تحميل مكتبة QRCode.js
        frappe.require("https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js", function () {
            // إنشاء QR Code داخل العنصر الجديد
            new QRCode(qr_div[0], {
                text: data_dict.generatedQR,
                width: 350,
                height: 350,
                correctLevel: QRCode.CorrectLevel.H,
                useSVG: true
            });

        });
        frm.toggle_display('custom_qr_code_html', true);

    }
});