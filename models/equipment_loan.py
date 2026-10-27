from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class EquipmentLoan(models.Model):
    _name = 'equipment.loan'
    _description = 'Equipment Loan'
    _order = 'loan_date desc'

    _unique_loan_fields = models.Constraint(
        'UNIQUE(employee_id,equipment_id,loan_date)',
        'This employee already has a loan for this equipment on this date.'
    )

    _check_duration_days = models.Constraint(
        'CHECK(duration_days > 0)',
        'Loan duration cannot be 0.'
    )

    name = fields.Char(string='Reference', default='New')
    employee_id = fields.Many2one(comodel_name='res.users', string='Employee')
    equipment_id = fields.Many2one(comodel_name='equipment.item', string='Equipment')
    daily_rate = fields.Float(related='equipment_id.daily_rate', string='Daily Rate', store=True)
    loan_date = fields.Date(string='Loan Date', default=fields.Date.today)
    return_date = fields.Date(string='Return Date')
    duration_days = fields.Integer(compute='_compute_duration_days', inverse='_inverse_duration_days', store=True, string='Duration Days')
    total_cost = fields.Float(compute='_compute_total_cost', store=True, string='Total Cost')
    state = fields.Selection(selection=[
        ('ongoing','Ongoing'),
        ('returned','Returned'),
    ], default='ongoing', string='State', readonly=True)

    @api.depends('loan_date', 'return_date')
    def _compute_duration_days(self):
        for loan in self:
            if loan.loan_date and loan.return_date:
                loan.duration_days = max((loan.return_date - loan.loan_date).days, 1)
            else:
                loan.duration_days = 1
    
    @api.depends('duration_days','daily_rate')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.duration_days * record.daily_rate
    
    @api.onchange('employee_id')
    def employee_loan_warning(self):
        if self.employee_id:
            count = self.search_count([('employee_id','=',self.employee_id.id),('state','=','ongoing')])
            if count >= 2:
                return {
                    "warning": {
                        "title": "Multiple Active Loans",
                        "message": f"{self.employee_id.name} already has {count} active loan(s).",
                    }
                }
    
    @api.constrains('loan_date','return_date')
    def _check_return_date(self):
        for record in self:
            if record.loan_date and record.return_date and record.return_date < record.loan_date:
                raise ValidationError(_('Return date cannot be earlier than loan date.'))
    
    def action_mark_returned(self):
        self.ensure_one()
        self.write({
            'return_date': fields.Date.today(),
            'state': 'returned'
        })
    
    def action_mark_cancelled(self):
        self.ensure_one()
        self.write({
            'state': 'ongoing'
        })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('equipment.loan') or _('New')
        return super(EquipmentLoan, self).create(vals_list)

    @api.constrains('equipment_id', 'state')
    def _check_equipment_available(self):
        for loan in self:
            if loan.state != 'ongoing' or not loan.equipment_id:
                continue
            other_loan = self.search([
                ('equipment_id', '=', loan.equipment_id.id),
                ('state', '=', 'ongoing'),
                ('id', '!=', loan.id),
            ], limit=1)
            if other_loan:
                raise ValidationError(_('This equipment is already borrowed.'))
    
    def _inverse_duration_days(self):
        for loan in self:
            if loan.loan_date:
                loan.return_date = loan.loan_date + timedelta(days=loan.duration_days)