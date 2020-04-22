# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import string


import logging
_logger = logging.getLogger(__name__)


class lov (models.Model):
    _inherit = 'stock.scrap'
    x_scrap_reason = fields.Selection([('Expired', 'Expired'),('Damage','Damage')], string='Scrap Reason')
   