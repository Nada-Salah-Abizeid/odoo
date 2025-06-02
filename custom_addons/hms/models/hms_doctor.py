from odoo import models, fields

class HmsDoctor(models.Model):
    _name= "hms.doctor"
    _description= "Doctor"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()

    department_id = fields.Many2one('hms.department', string='Department')
    patient_ids = fields.Many2many('hms.patient', 'doctor_ids', string='Patients')


