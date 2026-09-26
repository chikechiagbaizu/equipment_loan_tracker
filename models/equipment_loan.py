from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class EquipmentLoan(models.Model):
    _name = 'equipment.loan'
    _description = 'Equipment Loan'
    _rec_name = 'employee_id'
    _sql_constraints = [
        (
            'unique_loan_fields',
            'UNIQUE(employee_id,equipment_id,loan_date)',
            'This employee already has a loan for this equipment on this date.'
        ),
    ]

    employee_id = fields.Many2one(comodel_name='res.users', string='Employee')
    equipment_id = fields.Many2one(comodel_name='equipment.item', string='Equipment')
    daily_rate = fields.Float(related='equipment_id.daily_rate', string='Daily Rate', store=True)
    loan_date = fields.Date(string='Loan Date', default=fields.Date.today())
    return_date = fields.Date(string='Return Date')
    duration_days = fields.Integer(compute='_compute_duration_days', store=True, string='Duration Days')
    total_cost = fields.Float(compute='_compute_total_cost', store=True, string='Total Cost')
    state = fields.Selection(selection=[
        ('ongoing','Ongoing'),
        ('returned','Returned'),
    ], default='ongoing', string='State')

    @api.depends('loan_date','return_date')
    def _compute_duration_days(self):
        for record in self:
            end = record.return_date or date.today()
            record.duration_days = (end - record.loan_date).days
    
    @api.depends('duration_days','daily_rate')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.duration_days * record.daily_rate
    
    @api.onchange('employee_id')
    def employee_loan_warning(self):
        if self.employee_id:
            count = self.env['equipment.loan'].search_count([('employee_id','=',self.employee_id.id),('state','=','ongoing')])
            if count >= 2:
                return {
                    "warning": {
                        "title": "Multiple Active Loans",
                        "message": f"{self.employee_id.name} already has {count} active loan(s).",
                    }
                }
    
    @api.constrains('return_date')
    def return_date_constrains(self):
        for record in self:
            if record.return_date and record.return_date < record.loan_date:
                raise ValidationError("Return_date must never be earlier than loan_date.")
    
    def action_mark_returned(self):
        self.ensure_one()
        self.write({
            'return_date': fields.Date.today(),
            'state': 'returned'
        })
