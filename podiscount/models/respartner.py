# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import string


import logging
_logger = logging.getLogger(__name__)


class lov (models.Model):
    _inherit = 'res.partner'
    x_discount = fields.Float(string='Discount %',)


    @api.constrains('x_discount')
    def x_discount_constratints(self):
        if self.x_discount > 100 or self.x_discount < 0:
            raise ValidationError('Value should be between 0 - 100')
        
   