from odoo import models, fields

class HrJob(models.Model):
    _inherit = 'hr.job'

    position_type_id = fields.Many2one(
        'recruitment.position.type',
        string='Position Type',
        help='Select the position type to define skill requirements'
    )