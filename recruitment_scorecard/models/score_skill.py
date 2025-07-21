from odoo import models, fields, api

class ScoreSkill(models.Model):
    _name = 'recruitment.score.skill'
    _description = 'Score Skill for Recruitment'
    _order = 'name'

    name = fields.Char(string='Skill Name', required=True)
    description = fields.Text(string='Scoring Guidelines', help='Guidelines for scoring this skill from 1-10')
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Score skill name must be unique!'),
    ]