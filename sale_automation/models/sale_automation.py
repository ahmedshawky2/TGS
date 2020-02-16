# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import xlrd
from io import StringIO
from io import BytesIO
import base64
import logging
_logger = logging.getLogger(__name__)


class saleAutomation(models.Model):
    _name = 'sale_automation'
    _description = "Sale Automation"
    _order = 'write_date desc'



    name = fields.Char(string="Name", store=True, required=True, index=True, track_visibility='onchange',
                       default=lambda self: self.env['ir.sequence'].next_by_code('sale_automation_name'))

    status = fields.Selection([('New', 'New'), ('Success', 'Success'), ('Partial Success', 'Partial Success'),
                               ('Error', 'Error')], string="Status", store=True,
                              required=False, index=True, track_visibility='onchange', default='New')

    no_initial_rec = fields.Char(string="Number Of Records", store=True, index=True, track_visibility='onchange')

    no_success_rec = fields.Char(string="Number Of Success Orders", store=True, index=True, track_visibility='onchange')

    excel_file = fields.Binary(string='File for upload')

    confirm_so = fields.Boolean(string="Confirm SO", store=True, index=True,track_visibility='onchange')

    validate_delivery = fields.Boolean(string="Validate Delivery", store=True, index=True,track_visibility='onchange')

    create_invoice = fields.Boolean(string="Create Invoice", store=True, index=True,track_visibility='onchange')

    invoice_register_payment = fields.Boolean(string="Invoice Register Payment", store=True, index=True,track_visibility='onchange')

    error = fields.Text(string="Error", store=True, required=False)


    def runSA(self):

        try:

            inputx = BytesIO()
            _logger.info('inputx maged ! "%s"' % (str("inputx")))
            inputx.write(base64.decodestring(self.excel_file))
            book = xlrd.open_workbook(file_contents=inputx.getvalue())
            _logger.info('book maged ! "%s"' % (str(book)))

            # sheet = book.sheets()[0]
            sheet = book.sheet_by_index(0)
            _logger.info('sheet maged ! "%s"' % (str(sheet)))

            customerName = None
            customerId = None
            product = None
            productId = None
            productProductId = None
            productUnitPrice = None
            productDesc = None
            qty = None
            unitPrice = None
            taxes = None
            desc = None
            salesPerson = None
            salesPersonUserId = None
            salesPersonPartnerId = None
            sameInvoice = None

            lastOrderCheck = None
            createdOrderId = None

            saleOrderLineCreatedId = None

            saleOrderName = None
            saleOrderDeliveryName = None
            saleOrderDeliveryId = None

            deliveryIdLog = None
            invoiceIdLog = None
            saleOrderIdLog = None
            saleAutomationIdLog = self.id

            no_succ_rec = 0

            confirm_so = self.confirm_so
            validate_delivery = self.validate_delivery
            create_invoice = self.create_invoice
            invoice_register_payment = self.invoice_register_payment

            product_uom = self.env['uom.uom'].search([('name', '=', 'Unit(s)')])
            product_uom_id = int(product_uom[0]['id'])

            self.no_initial_rec = sheet.nrows

            for row_no in range(sheet.nrows):
                if row_no > 0:
                    deliveryIdLog = None
                    invoiceIdLog = None
                    try:
                        for col in range(sheet.ncols):
                            if col == 0:
                                _logger.info('Cell customerName ! "%s"' % (
                                            "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                        sheet.cell(row_no, col).value)))
                                customerName = str(sheet.cell(row_no, col).value)

                                customerId = self.env['res.partner'].search([('name', '=', customerName)])
                                customerId = customerId[0]['id']
                                _logger.info('customerId maged ! "%s"' % (str(customerId)))

                            elif col == 1:
                                _logger.info('Cell product ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                product = str(sheet.cell(row_no, col).value)

                                productProduct = self.env['product.product'].search([('default_code', '=', product)])
                                productProductId = productProduct[0]['id']
                                _logger.info('productProductId maged ! "%s"' % (str(productProductId)))

                                # product = self.env['product.template'].search([('default_code', '=', product)])
                                # productId = product[0]['id']
                                # _logger.info('productId maged ! "%s"' % (str(productId)))
                                # productUnitPrice = product[0]['list_price']
                                productUnitPrice = productProduct[0]['list_price']
                                _logger.info('productUnitPrice maged ! "%s"' % (str(productUnitPrice)))
                                # productDesc = product[0]['name']
                                productDesc = productProduct[0]['display_name']
                                _logger.info('productDesc maged ! "%s"' % (str(productDesc)))


                            elif col == 2:
                                _logger.info('Cell qty ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                qty = str(sheet.cell(row_no, col).value)

                            elif col == 3:
                                _logger.info('Cell unitPrice ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                unitPrice = str(sheet.cell(row_no, col).value)

                                if unitPrice is None or unitPrice == "":
                                    unitPrice = productUnitPrice


                            elif col == 4:
                                _logger.info('Cell taxes ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                taxes = str(sheet.cell(row_no, col).value)

                                if taxes is not None and taxes != "":
                                    taxes = int(float(taxes))
                                    _logger.info('taxes maged ! "%s"' % (str(taxes)))

                            elif col == 5:
                                _logger.info('Cell desc ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                desc = str(sheet.cell(row_no, col).value)

                                if desc is None or desc == "":
                                    desc = productDesc

                            elif col == 6:
                                _logger.info('Cell salesPerson ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                salesPerson = str(sheet.cell(row_no, col).value)

                                if salesPerson is not None and salesPerson != "":
                                    salesPersonPartnerId = self.env['res.partner'].search([('name', '=', salesPerson)])
                                    salesPersonPartnerId = salesPersonPartnerId[0]['id']

                                    salesPersonUserId = self.env['res.users'].search(
                                        [('partner_id', '=', salesPersonPartnerId)])
                                    salesPersonUserId = salesPersonUserId[0]['id']

                            elif col == 7:
                                _logger.info('Cell sameInvoice ! "%s"' % (
                                        "Row: " + str(row_no) + "   Col: " + str(col) + "   Cell Data: " + str(
                                    sheet.cell(row_no, col).value)))
                                sameInvoice = str(sheet.cell(row_no, col).value)

                        if sameInvoice != lastOrderCheck:
                            saleOrder = self.env['sale.order'].create({
                                'partner_id': customerId,
                                'user_id': salesPersonUserId,
                            })

                            createdOrderId = int(saleOrder)
                            saleOrderIdLog = int(saleOrder)
                            _logger.info('createdOrderId maged ! "%s"' % (str(createdOrderId)))

                        lastOrderCheck = sameInvoice

                        saleOrderLine = self.env['sale.order.line'].create({
                            'product_uom': product_uom_id,
                            'product_uom_qty': qty,
                            'order_partner_id': customerId,
                            'product_id': productProductId,
                            'order_id': createdOrderId,
                            'price_unit': unitPrice,
                            'name': desc,
                            # 'tax_id': taxes,
                        })

                        saleOrderLineCreatedId = int(saleOrderLine)
                        _logger.info('saleOrderLineCreatedId maged ! "%s"' % (str(saleOrderLineCreatedId)))

                        # _logger.info('row_no+1 maged ! "%s"' % (str(row_no+1)))
                        # _logger.info('sheet.nrows maged ! "%s"' % (str(sheet.nrows)))
                        # _logger.info('str(sheet.cell(row_no+1, 7).value) maged ! "%s"' % (str(sheet.cell(row_no+1, 7).value)))
                        # _logger.info('lastOrderCheck maged ! "%s"' % (str(lastOrderCheck)))
                        if row_no + 1 < sheet.nrows and str(sheet.cell(row_no + 1, 7).value) != lastOrderCheck:
                            saleOrderSearch = self.env['sale.order'].search([('id', '=', createdOrderId)])
                            _logger.info('saleOrderSearch maged ! "%s"' % (str(saleOrderSearch)))
                            if saleOrderSearch and confirm_so == True:
                                self.pool.get('sale.order').action_confirm(saleOrderSearch)

                                saleOrderName = saleOrderSearch[0]['name']
                                _logger.info('saleOrderName maged ! "%s"' % (str(saleOrderName)))

                                if saleOrderName is not None and saleOrderName != "":
                                    stockPickingSearch = self.env['stock.picking'].search(
                                        [('origin', '=', saleOrderName)])
                                    _logger.info('stockPickingSearch maged ! "%s"' % (str(stockPickingSearch)))

                                    if stockPickingSearch:
                                        saleOrderDeliveryName = stockPickingSearch[0]['name']
                                        _logger.info(
                                            'saleOrderDeliveryName maged ! "%s"' % (str(saleOrderDeliveryName)))

                                        if saleOrderDeliveryName is not None and saleOrderDeliveryName != "" and validate_delivery == True:
                                            saleOrderDeliveryId = stockPickingSearch[0]['id']
                                            deliveryIdLog = stockPickingSearch[0]['id']
                                            _logger.info(
                                                'saleOrderDeliveryId maged ! "%s"' % (str(saleOrderDeliveryId)))

                                            stockMoveSearch = self.env['stock.move'].search(
                                                [('picking_id', '=', saleOrderDeliveryId)])
                                            _logger.info('stockMoveSearch maged ! "%s"' % (str(stockMoveSearch)))

                                            for stockMoveLine in stockMoveSearch:
                                                _logger.info('stockMoveLine maged ! "%s"' % (str(stockMoveLine)))

                                                stockMoveLineSearch = self.env['stock.move.line'].search(
                                                    [('move_id', '=', stockMoveLine[0]['id'])])
                                                _logger.info(
                                                    'stockMoveLineSearch maged ! "%s"' % (str(stockMoveLineSearch)))

                                                if stockMoveLineSearch:
                                                    stockMoveLineSearch[0]['state'] = 'done'
                                                    stockMoveLineSearch[0]['qty_done'] = stockMoveLineSearch[0][
                                                        'product_uom_qty']

                                            _logger.info('stock.picking ==> button_validate start')
                                            self.pool.get('stock.picking').button_validate(stockPickingSearch)
                                            _logger.info('stock.picking ==> button_validate end')

                                            if create_invoice == True:
                                                _logger.info('sale.advance.payment.inv ==> create_invoices start')
                                                # self.pool.get('sale.advance.payment.inv').create_invoices(saleOrderSearch)
                                                payment = self.env['sale.advance.payment.inv'].with_context(
                                                    active_ids=[createdOrderId]).create({
                                                    'advance_payment_method': 'delivered'
                                                })
                                                payment.create_invoices()
                                                _logger.info('sale.advance.payment.inv ==> create_invoices end')

                                                accountInvoiceSearch = self.env['account.invoice'].search(
                                                    [('origin', '=', saleOrderName)])
                                                _logger.info(
                                                    'accountInvoiceSearch maged ! "%s"' % (str(accountInvoiceSearch)))

                                                if accountInvoiceSearch:
                                                    _logger.info('accountInvoiceSearch maged ! "%s"' % (
                                                        str(accountInvoiceSearch[0]['id'])))

                                                    invoiceIdLog = accountInvoiceSearch[0]['id']

                                                    _logger.info('account.invoice ==> action_invoice_open start')
                                                    self.pool.get('account.invoice').action_invoice_open(
                                                        accountInvoiceSearch)
                                                    _logger.info('account.invoice ==> action_invoice_open end')


                                                    if invoice_register_payment == True:
                                                        _logger.info(
                                                            'account.payment ==> action_validate_invoice_payment start')
                                                        # accountInvoiceSearch.invoice_ids = [accountInvoiceSearch[0]['id']]
                                                        # self.pool.get('account.payment').action_validate_invoice_payment(invoice_ids=[accountInvoiceSearch[0]['id']])
                                                        accountPayment = self.env['account.payment'].with_context(
                                                            active_ids=[accountInvoiceSearch[0]['id']],
                                                            active_id=accountInvoiceSearch[0]['id'],
                                                            invoice_ids=[accountInvoiceSearch[0]['id']]).create({
                                                            'payment_type': 'inbound',
                                                            'partner_type': 'customer',
                                                            'payment_method_id': 1,
                                                            'journal_id': 7,
                                                            'amount': accountInvoiceSearch[0]['amount_total'],
                                                        })
                                                        # inv = dict({"invoice_ids":accountInvoiceSearch[0]['id']})
                                                        # _logger.info('inv maged ! "%s"' % (str(inv.invoice_ids)))
                                                        if accountPayment.payment_type == 'transfer':
                                                            sequence_code = 'account.payment.transfer'
                                                        else:
                                                            if accountPayment.partner_type == 'customer':
                                                                if accountPayment.payment_type == 'inbound':
                                                                    sequence_code = 'account.payment.customer.invoice'
                                                                if accountPayment.payment_type == 'outbound':
                                                                    sequence_code = 'account.payment.customer.refund'
                                                            if accountPayment.partner_type == 'supplier':
                                                                if accountPayment.payment_type == 'inbound':
                                                                    sequence_code = 'account.payment.supplier.refund'
                                                                if accountPayment.payment_type == 'outbound':
                                                                    sequence_code = 'account.payment.supplier.invoice'
                                                        accountPayment.name = self.env['ir.sequence'].with_context(
                                                            ir_sequence_date=accountPayment.payment_date).next_by_code(
                                                            sequence_code)
                                                        accountPayment.invoice_ids = [accountInvoiceSearch[0]['id']]
                                                        accountPayment.action_validate_invoice_payment()
                                                        # self.pool.get('account.payment').action_validate_invoice_payment(
                                                        # self.env['account.payment'].search([('id', '=', int(accountPayment))]))
                                                        _logger.info('account.payment ==> action_validate_invoice_payment end')

                            no_succ_rec = no_succ_rec + 1

                            saleAutomationId = self.env['sale_automation_log'].create({
                                'sale_automation': saleAutomationIdLog,
                                'product_qty': qty,
                                'customer_id': customerId,
                                'product_id': productProductId,
                                'sale_order_id': saleOrderIdLog,
                                'product_unit_price': unitPrice,
                                'product_desc': desc,
                                'product_taxes': taxes,
                                'sales_person': salesPersonUserId,
                                'product_same_inv': sameInvoice,
                                'delivery_id': deliveryIdLog,
                                'inv_id': invoiceIdLog,
                                'confirm_so': confirm_so,
                                'validate_delivery': validate_delivery,
                                'create_invoice': create_invoice,
                                'invoice_register_payment': invoice_register_payment,
                                'status': 'Success',
                            })


                        if row_no + 1 == sheet.nrows:
                            saleOrderSearch = self.env['sale.order'].search([('id', '=', createdOrderId)])
                            _logger.info('saleOrderSearch maged ! "%s"' % (str(saleOrderSearch)))
                            if saleOrderSearch and confirm_so == True:
                                self.pool.get('sale.order').action_confirm(saleOrderSearch)

                                saleOrderName = saleOrderSearch[0]['name']
                                _logger.info('saleOrderName maged ! "%s"' % (str(saleOrderName)))

                                if saleOrderName is not None and saleOrderName != "":
                                    stockPickingSearch = self.env['stock.picking'].search(
                                        [('origin', '=', saleOrderName)])
                                    _logger.info('stockPickingSearch maged ! "%s"' % (str(stockPickingSearch)))

                                    if stockPickingSearch:
                                        saleOrderDeliveryName = stockPickingSearch[0]['name']
                                        _logger.info(
                                            'saleOrderDeliveryName maged ! "%s"' % (str(saleOrderDeliveryName)))

                                        if saleOrderDeliveryName is not None and saleOrderDeliveryName != "" and validate_delivery == True:
                                            saleOrderDeliveryId = stockPickingSearch[0]['id']
                                            deliveryIdLog = stockPickingSearch[0]['id']
                                            _logger.info(
                                                'saleOrderDeliveryId maged ! "%s"' % (str(saleOrderDeliveryId)))

                                            stockMoveSearch = self.env['stock.move'].search(
                                                [('picking_id', '=', saleOrderDeliveryId)])
                                            _logger.info('stockMoveSearch maged ! "%s"' % (str(stockMoveSearch)))

                                            for stockMoveLine in stockMoveSearch:
                                                _logger.info('stockMoveLine maged ! "%s"' % (str(stockMoveLine)))

                                                stockMoveLineSearch = self.env['stock.move.line'].search(
                                                    [('move_id', '=', stockMoveLine[0]['id'])])
                                                _logger.info(
                                                    'stockMoveLineSearch maged ! "%s"' % (str(stockMoveLineSearch)))

                                                if stockMoveLineSearch:
                                                    stockMoveLineSearch[0]['state'] = 'done'
                                                    stockMoveLineSearch[0]['qty_done'] = stockMoveLineSearch[0][
                                                        'product_uom_qty']

                                            _logger.info('stock.picking ==> button_validate start')
                                            self.pool.get('stock.picking').button_validate(stockPickingSearch)
                                            _logger.info('stock.picking ==> button_validate end')

                                            if create_invoice == True:
                                                _logger.info('sale.advance.payment.inv ==> create_invoices start')
                                                # self.pool.get('sale.advance.payment.inv').create_invoices(saleOrderSearch)
                                                payment = self.env['sale.advance.payment.inv'].with_context(
                                                    active_ids=[createdOrderId]).create({
                                                    'advance_payment_method': 'delivered'
                                                })
                                                payment.create_invoices()
                                                _logger.info('sale.advance.payment.inv ==> create_invoices end')

                                                accountInvoiceSearch = self.env['account.invoice'].search(
                                                    [('origin', '=', saleOrderName)])
                                                _logger.info(
                                                    'accountInvoiceSearch maged ! "%s"' % (str(accountInvoiceSearch)))

                                                if accountInvoiceSearch:
                                                    _logger.info('accountInvoiceSearch maged ! "%s"' % (
                                                        str(accountInvoiceSearch[0]['id'])))

                                                    invoiceIdLog = accountInvoiceSearch[0]['id']

                                                    _logger.info('account.invoice ==> action_invoice_open start')
                                                    self.pool.get('account.invoice').action_invoice_open(
                                                        accountInvoiceSearch)
                                                    _logger.info('account.invoice ==> action_invoice_open end')

                                                    if invoice_register_payment == True:
                                                        _logger.info(
                                                            'account.payment ==> action_validate_invoice_payment start')
                                                        # accountInvoiceSearch.invoice_ids = [accountInvoiceSearch[0]['id']]
                                                        # self.pool.get('account.payment').action_validate_invoice_payment(invoice_ids=[accountInvoiceSearch[0]['id']])
                                                        accountPayment = self.env['account.payment'].with_context(
                                                            active_ids=[accountInvoiceSearch[0]['id']],
                                                            active_id=accountInvoiceSearch[0]['id'],
                                                            invoice_ids=[accountInvoiceSearch[0]['id']]).create({
                                                            'payment_type': 'inbound',
                                                            'partner_type': 'customer',
                                                            'payment_method_id': 1,
                                                            'journal_id': 7,
                                                            'amount': accountInvoiceSearch[0]['amount_total'],
                                                        })
                                                        # inv = dict({"invoice_ids":accountInvoiceSearch[0]['id']})
                                                        # _logger.info('inv maged ! "%s"' % (str(inv.invoice_ids)))
                                                        if accountPayment.payment_type == 'transfer':
                                                            sequence_code = 'account.payment.transfer'
                                                        else:
                                                            if accountPayment.partner_type == 'customer':
                                                                if accountPayment.payment_type == 'inbound':
                                                                    sequence_code = 'account.payment.customer.invoice'
                                                                if accountPayment.payment_type == 'outbound':
                                                                    sequence_code = 'account.payment.customer.refund'
                                                            if accountPayment.partner_type == 'supplier':
                                                                if accountPayment.payment_type == 'inbound':
                                                                    sequence_code = 'account.payment.supplier.refund'
                                                                if accountPayment.payment_type == 'outbound':
                                                                    sequence_code = 'account.payment.supplier.invoice'
                                                        accountPayment.name = self.env['ir.sequence'].with_context(
                                                            ir_sequence_date=accountPayment.payment_date).next_by_code(
                                                            sequence_code)
                                                        accountPayment.invoice_ids = [accountInvoiceSearch[0]['id']]
                                                        accountPayment.action_validate_invoice_payment()
                                                        # self.pool.get('account.payment').action_validate_invoice_payment(
                                                        # self.env['account.payment'].search([('id', '=', int(accountPayment))]))
                                                        _logger.info(
                                                            'account.payment ==> action_validate_invoice_payment end')

                            no_succ_rec = no_succ_rec + 1

                            saleAutomationId = self.env['sale_automation_log'].create({
                                'sale_automation': saleAutomationIdLog,
                                'product_qty': qty,
                                'customer_id': customerId,
                                'product_id': productProductId,
                                'sale_order_id': saleOrderIdLog,
                                'product_unit_price': unitPrice,
                                'product_desc': desc,
                                'product_taxes': taxes,
                                'sales_person': salesPersonUserId,
                                'product_same_inv': sameInvoice,
                                'delivery_id': deliveryIdLog,
                                'inv_id': invoiceIdLog,
                                'confirm_so': confirm_so,
                                'validate_delivery': validate_delivery,
                                'create_invoice': create_invoice,
                                'invoice_register_payment': invoice_register_payment,
                                'status': 'Success',
                            })

                    except Exception as e:
                        _logger.info(u'ERROR: {}'.format(e))
                        self.status = 'Partial Success'
                        saleAutomationId = self.env['sale_automation_log'].create({
                            'sale_automation': saleAutomationIdLog,
                            'product_qty': qty,
                            'customer_id': customerId,
                            'product_id': productProductId,
                            'sale_order_id': saleOrderIdLog,
                            'product_unit_price': unitPrice,
                            'product_desc': desc,
                            'product_taxes': taxes,
                            'sales_person': salesPersonUserId,
                            'product_same_inv': sameInvoice,
                            'delivery_id': deliveryIdLog,
                            'inv_id': invoiceIdLog,
                            'confirm_so': confirm_so,
                            'validate_delivery': validate_delivery,
                            'create_invoice': create_invoice,
                            'invoice_register_payment': invoice_register_payment,
                            'status': 'Error',
                            'error': u'ERROR: {}'.format(e),
                        })
                        pass
                        # raise ValidationError(u'ERROR: {}'.format(e))

            self.no_success_rec = no_succ_rec
            self.status = 'Success'
        except Exception as e:
            _logger.info(u'ERROR: {}'.format(e))
            self.status = 'Error'
            self.error = u'ERROR: {}'.format(e)
            self.no_success_rec = no_succ_rec