# -*- coding: utf-8 -*-

from odoo import models, fields


class OpEvaluationType(models.Model):
    _name = "op.evaluation.type"
    _description = "Course evaluation type"

    name = fields.Char('Name', size=128, required=True)
