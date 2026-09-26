{
    'name': 'Equipment Loan Tracker',
    'summary': 'Equipment Loan Tracker',
    'description': """
    An Odoo module for tracking company equipment (laptops, tools, and other assets) loaned out to employees — who has what, since when, and what it's costing.
    """,
    'author': 'Chike Chiagbaizu',
    'maintainer': 'Chike Chiagbaizu',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'category': 'Human Resources',
    'application': True,
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        'security/group_equipment_manager.xml',
        'security/ir.model.access.csv',
        'security/rule_equipment_user.xml',
        'wizard/bulk_return_wizard_view.xml',
        'views/view_equipment_item_form.xml',
        'views/view_equipment_item_list.xml',
        'views/view_equipment_loan_form.xml',
        'views/view_equipment_loan_list.xml',
        'views/equipment_actions.xml',
        'views/equipment_menus.xml',
    ]
}