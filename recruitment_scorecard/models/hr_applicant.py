from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    candidate_scores = fields.One2many(
        'recruitment.candidate.score',
        'applicant_id',
        string='Candidate Scores'
    )
    
    # Agregar este campo calculado
    has_skills_below_minimum = fields.Boolean(
        string='Has Skills Below Minimum',
        compute='_compute_skills_below_minimum',
        store=True
    )
    
    @api.depends('candidate_scores.is_below_minimum')
    def _compute_skills_below_minimum(self):
        for record in self:
            # Verifica si algún score está por debajo del mínimo
            record.has_skills_below_minimum = any(
                score.is_below_minimum for score in record.candidate_scores
            )
    
    @api.model
    def create(self, vals):
        applicant = super(HrApplicant, self).create(vals)
        applicant._create_candidate_scores()
        return applicant
    
    def write(self, vals):
        result = super(HrApplicant, self).write(vals)
        if 'job_id' in vals:
            for applicant in self:
                applicant._create_candidate_scores()
        return result
    
    def _create_candidate_scores(self):
        """Create candidate scores based on job position type"""
        if not self.job_id or not self.job_id.position_type_id:
            return
        
        # Remove existing scores
        self.candidate_scores.unlink()
        
        # Create new scores based on position type requirements
        for requirement in self.job_id.position_type_id.skill_requirements:
            self.env['recruitment.candidate.score'].create({
                'applicant_id': self.id,
                'score_skill_id': requirement.score_skill_id.id,
                'minimum_required': requirement.minimum_score,
                'score': 0,
            })

class CandidateScore(models.Model):
    _name = 'recruitment.candidate.score'
    _description = 'Candidate Score for Skills'
    _order = 'score_skill_id'

    applicant_id = fields.Many2one(
        'hr.applicant',
        string='Applicant',
        required=True,
        ondelete='cascade'
    )
    score_skill_id = fields.Many2one(
        'recruitment.score.skill',
        string='Score Skill',
        required=True
    )
    score = fields.Integer(
        string='Score',
        default=0
    )
    minimum_required = fields.Integer(
        string='Minimum Required',
        readonly=True
    )
    is_below_minimum = fields.Boolean(
        string='Below Minimum',
        compute='_compute_is_below_minimum',
        store=True
    )
    skill_description = fields.Text(
        related='score_skill_id.description',
        string='Scoring Guidelines'
    )
    
    @api.depends('score', 'minimum_required')
    def _compute_is_below_minimum(self):
        for record in self:
            record.is_below_minimum = record.score > 0 and record.score < record.minimum_required
    
    @api.constrains('score')
    def _check_score_range(self):
        for record in self:
            if record.score < 0 or record.score > 10:
                raise ValidationError('Score must be between 0 and 10')