from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    @api.constrains('related_patient_id', 'email')
    def check_unique_patient_email(self):
        for rec in self:
            if rec.email == rec.related_patient_id.email:
                raise ValidationError("Patient email must be unique.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient.")
        return super().unlink()
