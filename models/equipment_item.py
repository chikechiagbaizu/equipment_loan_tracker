from odoo import models, fields, api

class EquipmentItem(models.Model):
    _name = 'equipment.item'
    _description = 'Equipment Item'

    name = fields.Char(string='Equipment Name', required=True)
    category = fields.Selection(selection=[
        ('laptop','Laptop'),
        ('tool','Tool'),
        ('other','Other'),
    ], string='Category')
    daily_rate = fields.Float(string='Daily Rate')
    active = fields.Boolean(string='Active', default=True)
    loan_ids = fields.One2many(comodel_name='equipment.loan', inverse_name='equipment_id', string='Loans')