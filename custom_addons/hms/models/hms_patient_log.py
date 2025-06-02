from odoo import models, fields

class HMSPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    description = fields.Text()
    patient_id = fields.Many2one('hms.patient', string="Patient")