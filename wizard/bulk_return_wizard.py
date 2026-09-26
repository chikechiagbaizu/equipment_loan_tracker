from odoo import models, fields
from datetime import date

class BulkReturnWizard(models.TransientModel):
    _name = 'bulk.return.wizard'
    _description = 'Bulk Return Wizard'
    
    return_date = fields.Date(string='Return Date', required=True)

    def action_bulk_return(self):
        active_ids = self.env.context.get('active_ids')
        loans = self.env['equipment.loan'].browse(active_ids)

        for loan in loans:
            loan.write({
                'return_date': self.return_date,
                'state': 'returned'
            })