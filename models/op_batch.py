# -*- coding: utf-8 -*-

from odoo import fields, models, api
from requests import get, post
import logging

logger = logging.getLogger(__name__)

TOKEN = "3de3ace98f80a5b1e16c84a378d72741"
URL = "https://isep.moodlecloud.com"
ENDPOINT = "/webservice/rest/server.php"


class op_batch(models.Model):
    _inherit = "op.batch"

    anyacademico = fields.Char("Año académico", size=20)
    nivel = fields.Char("Nivel", size=10)
    duracion = fields.Integer("Duracion", default=0)
    ciudad = fields.Char("Ciudad", size=50)
    diasemana = fields.Char("Dia de la semana", size=50)
    titulo = fields.Char("Titulo", size=200)
    titulo_catalan = fields.Char("Título catalán", size=200)
    lugarclase = fields.Char("Lugar de Clase", size=200)
    horario = fields.Char("Horario", size=200)
    coordinador = fields.Many2one('op.faculty', string="Coordinador")
    departamento = fields.Char("Departamento", size=20)
    modalidad_id = fields.Many2one('op.modalidad', string='Modalidad')
    universidad = fields.Char("Universidad", size=10)
    marca = fields.Char("Marca", size=10)
    tutor = fields.Char("Tutor", size=50)
    horariotutor = fields.Char("Horario tutor", size=100)
    solicitud = fields.Char("Solicitud", size=50)
    idioma = fields.Many2one('res.lang', string='Idioma')
    totalhoras = fields.Float("Total de Horas")
    totalcreditos = fields.Float("Total de crédito")
    gin_oldcursoid = fields.Char("OldCursoID", size=100)
    gin_codigohorario = fields.Char("Codigo Horario", size=100)
    gin_oldnombrecurso = fields.Char("OldNombreCurso", size=100)
    reconocimientos = fields.Char("Reconocimientos", size=700)
    reconeixements = fields.Char("Reconeixements", size=700)

    codigouvic = fields.Char("Codigo UVic", size=50)
    contenido = fields.Char("Contenido", size=1024)
    diasvencimiento = fields.Integer("Dias de vencimiento", default=0)
    convocatoriauvic = fields.Integer("Convocatoria UVic", default=0)
    programauvic = fields.Char("Programa UVic", size=50)
    grupbaixtemporal = fields.Integer("Grupo Baja Temporal", default=0)
    anyinicio = fields.Char("Año inicio", size=50)
    campanya = fields.Char("Campaña", size=50)
    fechadiplomas = fields.Datetime("Fecha diplomas")
    moodleid = fields.Char("MoodleId", size=20)
    moodleid2 = fields.Char("MoodleId2", size=64)
    fechabaja = fields.Datetime("Fecha baja")
    external_id = fields.Integer("External_id")

    op_batch_subject_rel_ids = fields.One2many('op.batch.subject.rel', 'id')
    student_lines = fields.One2many('op.student.course', 'id')
    moodle_course_id = fields.Integer(string="Moodle Id")

    @api.model
    def create(self, values):
        logger.info("On create course")
        params = {
            'courses[0][fullname]': values.get('name'),
            'courses[0][shortname]': values.get('code'),
            'courses[0][idnumber]': values.get('code'),
            'courses[0][summary]': values.get('name'),
            'courses[0][summaryformat]': 1,
            'courses[0][format]': 'topics',
            'courses[0][numsections]': 8,
            'courses[0][showreports]': 1,
            'courses[0][visible]': 1,
            'courses[0][lang]': 'en',
            'courses[0][categoryid]': 3,
            "wstoken": TOKEN,
            'moodlewsrestformat': 'json',
            "wsfunction": 'core_course_create_courses'
        }
        try:
            response = post(URL + ENDPOINT, params)
            response = response.json()
            logger.info(type(response))
            logger.info(response)
            if type(response) == dict and response.get('exception'):
                raise logger.info(response.get('exception'))
            else:
                logger.info(response[0].get('id'))
                values.update({'moodle_course_id': response[0].get('id')})
        except Exception:
            logger.info("Error")
            logger.info(Exception)
            raise logger.info("Error calling Moodle API\n", Exception)
        res = super(op_batch, self).create(values)
        return res

    @api.multi
    def write(self, values):
        logger.info("On update course")
        params = {
            'courses[0][id]': self.moodle_course_id,
            'courses[0][fullname]': values.get('name'),
            'courses[0][shortname]': values.get('code'),
            'courses[0][idnumber]': values.get('code'),
            'courses[0][summary]': values.get('name'),
            "wstoken": TOKEN,
            'moodlewsrestformat': 'json',
            "wsfunction": 'core_course_update_courses'
        }
        try:
            response = post(URL + ENDPOINT, params)
            response = response.json()
            logger.info(response)
            if type(response) == dict and response.get('exception'):
                raise logger.info("Error calling Moodle API\n", response)
        except ValueError:
            logger.info("Error")
            logger.info(ValueError)
            raise logger.info("Error calling Moodle API\n", ValueError)
        res = super(op_batch, self).write(values)
        return res
