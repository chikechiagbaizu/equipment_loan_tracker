from odoo import models, fields

class EquipmentItem(models.Model):
    _name = 'equipment.item'
    _description = 'Equipment Item'

    EQUIPMENT_CATEGORIES = [
    ('it_computing', 'IT and Computing Equipment'),
    ('audio_visual', 'Audio-Visual and Presentation Equipment'),
    ('tools_maintenance', 'Tools and Maintenance Equipment'),
    ('safety_protective', 'Safety and Protective Equipment'),
    ('vehicles_transport', 'Vehicles and Transport Equipment'),
    ]

    name = fields.Char(string='Equipment Name', default="it_computing", required=True)
    category = fields.Selection(selection=EQUIPMENT_CATEGORIES, string='Equipment Category')
    daily_rate = fields.Float(string='Daily Rate')
    active = fields.Boolean(string='Active', default=True)
    loan_ids = fields.One2many(comodel_name='equipment.loan', inverse_name='equipment_id', string='Loans')