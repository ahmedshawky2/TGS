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
    _name = 'sale_automation_log'
    _description = "Sale Automation Log"
    _order = 'write_date desc'



    sale_automation = fields.Many2one(comodel_name="sale_automation", string="Sale Automation", store=True, required=True, index=True)

    status = fields.Selection([('New', 'New'), ('Success', 'Success'),('Error', 'Error')], string="Status", store=True,
                              required=False, index=True, track_visibility='onchange', default='New')

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", store=True, required=True, index=True)

    product_id = fields.Many2one(comodel_name="product.product", string="Product", store=True, required=True, index=True)

    product_qty = fields.Char(string="Product Qty", store=True, required=True, index=True)

    product_unit_price = fields.Char(string="Product Unit Price", store=True, required=False, index=True)

    product_taxes = fields.Char(string="Product Taxes", store=True, required=False, index=True)

    product_desc = fields.Char(string="Product Description", store=True, required=False)

    sales_person = fields.Many2one(comodel_name="res.users", string="Sales Person", store=True, required=False, index=True)

    product_same_inv = fields.Char(string="Product Same Invoice", store=True, required=True, index=True)

    account_journal = fields.Char(string="Account Journal", store=True, required=True, index=True)

    payment_amount_money = fields.Char(string="Payment Amount Money", store=True, required=True, index=True)

    payment_amount_percent = fields.Char(string="Payment Amount Percent", store=True, required=True, index=True)

    payment_amount_final = fields.Char(string="Payment Amount Final", store=True, required=True, index=True)

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sales Order", store=True, required=False, index=True)

    delivery_id = fields.Many2one(comodel_name="stock.picking", string="Delivery", store=True, required=False, index=True)

    inv_id = fields.Many2one(comodel_name="account.invoice", string="Invoice", store=True, required=False, index=True)

    error = fields.Text(string="Error", store=True, required=False)

    confirm_so = fields.Boolean(string="Confirm SO", store=True, index=True, track_visibility='onchange')

    validate_delivery = fields.Boolean(string="Validate Delivery", store=True, index=True, track_visibility='onchange')

    create_invoice = fields.Boolean(string="Create Invoice", store=True, index=True, track_visibility='onchange')

    invoice_register_payment = fields.Boolean(string="Invoice Register Payment", store=True, index=True,
                                              track_visibility='onchange')

