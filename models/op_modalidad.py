# -*- coding: utf-8 -*-

from odoo import models, fields


class OpModalidad(models.Model):
    _name = "op.modalidad"
    _description = "Modalidad"

    name = fields.Char('Name', size=128, required=True)
