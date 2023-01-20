from __future__ import unicode_literals
import frappe

def execute():
    doc = frappe.get_doc('System Settings')
    doc.email_footer_address = """<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed;" width="100%">
        <tbody><tr>
            <td style="color: #000000; font-size: 12px; font-family: Arial, Helvetica, sans-serif; font-weight: normal;">Thanks &amp; Regards,
            </td>
        </tr>
        </tbody><tbody>

            <tr>
                <td>
                    <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed;">
                        <tbody>
                            <tr>
                                <td style="padding-right: 15px; vertical-align: top; font-family: Arial, Helvetica, sans-serif;">
                                    <br><table style="border-collapse: collapse; table-layout: fixed;">

                                        <tbody>
                                            
                                            <tr>
                                                <td style="height: 100px;">
                                                    <img alt="logo" border="0" height="126" src="https://ci3.googleusercontent.com/mail-sig/AIorK4wM8Q43rx_vmlBjWrd2a1YKcJiLNMv5ZEeHH9OST8ue0385nHjb4OULPTl-xdXHDzbsZTQijUE" style="display: block; border: 0px; border-radius: 0px;">
                                                    
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td style="vertical-align: top; font-family: Arial, Helvetica, sans-serif; border-left: 3px ; padding-left: 15px;">
                                    <br><table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed;" width="500%">
                                        <tbody>
                                            
                                            <tr>
                                                <td style="color: #000000; font-size: 18px; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 15px; padding-bottom: 2px; padding-top: 10px;">Accounts Department</td>
                                            </tr>
                                             <tr>
                                                <td style="color: #000000; font-size: 13px; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 15px; padding-bottom: 5px;">Goregaon - Mumbai 400063</td>
                                            </tr>
                                            <tr>
                                                
                                            </tr>
                                            <tr>
                                                <td style="color: #000000; text-decoration: none; font-size: 12px; font-family: Arial, Helvetica, sans-serif; font-weight: normal; line-height: 15px; padding-bottom: 2px;">022-69121149 </td>
                                            </tr>
                                            <tr>
                                                <td style="padding-bottom: 5px;">
                                                    <a href="https://accounts@1finance.co.in" style="color: #0000ff; text-decoration: underline; font-size: 12px; font-family: Arial, Helvetica, sans-serif; font-weight: normal; line-height: 15px; padding-bottom: 5px;" target="_blank">accounts@1finance.co.in</a> | <a href="https://www.1finance.co.in" style="color: #1155cc; text-decoration: underline; font-size: 12px; font-family: Arial, Helvetica, sans-serif; font-weight: normal; line-height: 15px; padding-bottom: 2px;" target="_blank">www.1finance.co.in</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #000000; font-size: 12px; font-family: Arial, Helvetica, sans-serif; font-weight: normal; line-height: 15px; padding-bottom: 10px;">Marwadi Chandarana Group
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding-top: 7.5px;">
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>

</td></tr></tbody></table>"""
    doc.save()
    frappe.db.commit()