{
    'name': 'Recruitment Score Card',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Score card system for recruitment candidates',
    'description': """
        This module adds a score card system to the recruitment app:
        - Score Skills with ratings from 1-10
        - Position Types with minimum skill requirements
        - Candidate scoring with visual indicators
        - Helper tooltips for consistent scoring
    """,
    'author': 'Israel Santana',
    'depends': ['hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/score_skill_views.xml',
        'views/position_type_views.xml',
        'views/hr_job_views.xml',
        'views/hr_applicant_views.xml',
        'data/score_skill_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'recruitment_scorecard/static/src/css/scorecard.css',
            'recruitment_scorecard/static/src/js/scorecard.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}