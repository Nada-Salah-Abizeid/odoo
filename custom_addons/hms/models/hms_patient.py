from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    state = fields.Selection(
        [('undetermined', 'Undetermined'), ('good', 'Good'), ('fair', 'Fair'), ('serious', 'Serious'), ],
        default='undetermined')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    department_id = fields.Many2one('hms.department', string='Department', domain="[('is_opened','=',True)]")
    department_capacity = fields.Integer(string="Department Capacity", related='department_id.capacity', store=True)
    patient_logs = fields.One2many('hms.patient.log', 'patient_id', string='Patient Logs')
    age = fields.Integer(compute="calculate_age", store=True)
    email= fields.Char()

    _sql_constraints = [('unique_email', 'UNIQUE(email)', "Email can't be duplicated.")]

    def create_patient_log(self):
        vals = {
            'description': "State changed to %s" % (self.state),
            'patient_id': self.id
        }
        self.env['hms.patient.log'].create(vals)


    @api.depends('birth_date')
    def calculate_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth_date = record.birth_date
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0

    def action_undetermined(self):
        self.state = 'undetermined'

    def action_good(self):
        self.state = 'good'

    def action_fair(self):
        self.state = 'fair'

    def action_serious(self):
        self.state = 'serious'

    @api.onchange('doctor_ids')
    def doctor_selection_without_department(self):
        if not self.department_id and self.doctor_ids:
            self.doctor_ids = False
            return {
                'warning': {
                    'title': "Blocked",
                    'message': "You must select a department first."
                }
            }

    # @api.onchange('pcr')
    # def check_cr_mandatory(self):
    #     if self.pcr and not self.cr_ratio:
    #         return {
    #             'warning': {
    #                 'title': ('CR is Mandatory'),
    #                 'message': f'Must choose CR ratio. '
    #             }
    #         }

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR ratio is required when PCR is checked.")


    @api.onchange('age')
    def onchange_age(self):
        if self.age and self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR was automatically checked because the patient's age is below 30."
                }
            }