# Equipment Loan Tracker

An Odoo module for tracking company equipment (laptops, tools, and other assets) loaned out to employees — who has what, since when, and what it's costing.

Built as a hands-on learning project to practice core Odoo development patterns: computed fields, onchange warnings, model constraints, wizards, and row-level security.

## Features

- **Equipment master data** — register laptops, tools, and other assets with a daily rate.
- **Loan tracking** — record which employee has which item, from what date.
- **Automatic cost calculation** — duration and total cost are computed automatically, live, whether the item has been returned or is still out.
- **Overload warning** — a non-blocking warning appears when assigning a loan to an employee who already has 2+ active loans.
- **Data integrity rules**
  - A return date can never be earlier than the loan date.
  - The same employee can't be loaned the same equipment on the same date twice (enforced at the database level).
- **Bulk return** — select multiple active loans from the list view and return them all at once via a wizard.
- **Role-based access**
  - **Equipment Managers** can view and manage all loans.
  - **Regular users** can only see their own loans.

## Models

| Model | Purpose |
|---|---|
| `equipment.item` | Master data for loanable equipment (name, category, daily rate) |
| `equipment.loan` | A single loan record linking an employee to an equipment item |
| `bulk.return.wizard` | Transient wizard for returning multiple loans in one action |

## Installation

1. Copy the `equipment_loan_tracker` folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Activate developer mode, go to **Apps**, click **Update Apps List**.
4. Search for "Equipment Loan Tracker" and click **Install**.

## Usage

1. Go to **Equipment Loans → Configuration → Equipment** to register your equipment.
2. Go to **Equipment Loans → Loans** to create a new loan, assigning an employee and an equipment item.
3. Use the **Mark Returned** button on an individual loan, or select multiple loans in the list view and use the **Bulk Return** action, to close out loans.
4. Assign the **Equipment Manager** group (under Settings → Users) to anyone who should see and manage all loans rather than just their own.

## Folder structure

```
equipment_loan_tracker/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── equipment_item.py
│   └── equipment_loan.py
├── wizard/
│   ├── __init__.py
│   ├── bulk_return_wizard.py
│   └── bulk_return_wizard_views.xml
├── security/
│   ├── equipment_security.xml
│   ├── equipment_loan_rule.xml
│   └── ir.model.access.csv
└── views/
    ├── equipment_item_views.xml
    ├── equipment_loan_views.xml
    ├── equipment_actions.xml
    └── equipment_menus.xml
```

## Requirements

- Odoo 17.0+
- No external Python dependencies beyond Odoo core

## License

LGPL-3

## Author

Chike Chiagbaizu