# -*- coding: utf-8 -*-

from odoo import models, fields


class Subjects(models.Model):
    _inherit = 'op.subject'

    moodle_course_id = fields.Integer(string='Moodle course Id')
