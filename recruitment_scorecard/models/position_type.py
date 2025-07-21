from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PositionType(models.Model):
    _name = 'recruitment.position.type'
    _description = 'Position Type for Recruitment'
    _order = 'name'

    name = fields.Char(string='Position Type', required=True)
    description = fields.Text(string='Description')
    skill_requirements = fields.One2many(
        'recruitment.position.skill.requirement',
        'position_type_id',
        string='Skill Requirements'
    )
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Position type name must be unique!'),
    ]

class PositionSkillRequirement(models.Model):
    _name = 'recruitment.position.skill.requirement'
    _description = 'Skill Requirement for Position Type'
    _order = 'score_skill_id'

    position_type_id = fields.Many2one(
        'recruitment.position.type',
        string='Position Type',
        required=True,
        ondelete='cascade'
    )
    score_skill_id = fields.Many2one(
        'recruitment.score.skill',
        string='Score Skill',
        required=True
    )
    minimum_score = fields.Integer(
        string='Minimum Score',
        required=True,
        default=1
    )
    
    @api.constrains('minimum_score')
    def _check_minimum_score(self):
        for record in self:
            if not (1 <= record.minimum_score <= 10):
                raise ValidationError('Minimum score must be between 1 and 10')
    
    _sql_constraints = [
        ('unique_skill_per_position', 'unique(position_type_id, score_skill_id)', 
         'Each skill can only be added once per position type!'),
    ]