# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
import string


import logging
_logger = logging.getLogger(__name__)


class purchase_order (models.Model):
    _inherit = 'purchase.order.line'



    def _prepare_account_move_line(self, move):
        #raise ValidationError("test")
        x_discount = self.env.context.get('default_x_discount', 0)
        res = super()._prepare_account_move_line(move)
        #_logger.debug("Shawky  %s" ,res)
        res.update({
                'discount': x_discount,
                
                })
        return res

    


    '''
    def _prepare_account_move_line(self, move):
        self.ensure_one()
        raise ValidationError("test")
        if self.product_id.purchase_method == 'purchase':
            qty = self.product_qty - self.qty_invoiced
        else:
            qty = self.qty_received - self.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
            qty = 0.0

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        return {
            'name': '%s: %s' % (self.order_id.name, self.name),
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'purchase_line_id': self.id,
            'date_maturity': move.invoice_date_due,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'partner_id': move.partner_id.id,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
        }
    '''
    
   