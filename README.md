# Equipment Loan Tracker

An Odoo module for tracking company equipment (laptops, projectors, tools, safety gear, vehicles) loaned out to employees: who has what, since when, for how long, and what it costs.

Built as a hands-on learning project to practice core Odoo development patterns: sequences, computed fields with inverses, constraints, wizards, and record rules.

## Features

- **Equipment master data**: register items with a category and a daily rate.
- **Equipment categories**: IT and Computing, Audio-Visual and Presentation, Tools and Maintenance, Safety and Protective, Vehicles and Transport.
- **Auto-generated loan reference**: each loan gets a unique number from an `ir.sequence`, e.g. `LOAN/2026/00001`.
- **Two-way date and duration**: enter a return date and the duration is computed, or enter a number of days and the return date is set from the loan date.
- **Automatic cost calculation**: total cost is duration × daily rate, updated live.
- **Minimum billable day**: same-day returns and open loans count as 1 day, so duration is never 0.
- **Overload warning**: a non-blocking warning appears when an employee already has 2 or more active loans.
- **Data integrity rules**
  - Equipment already on an ongoing loan cannot be loaned again until it is returned. This is checked for batch creates and edits too.
  - A return date can never be earlier than the loan date.
  - The same employee cannot borrow the same equipment on the same date twice.
  - Loan duration must be at least 1 day (database constraint).
- **Bulk return**: select several loans in the list view and return them all with one chosen return date.
- **Role-based access**
  - **Equipment Managers** can view and manage all loans.
  - **Regular users** can only see and edit their own loans.

## Models

| Model | Purpose |
|---|---|
| `equipment.item` | Master data for loanable equipment (name, category, daily rate) |
| `equipment.loan` | A loan linking an employee to an equipment item, with state (`ongoing` / `returned`) |
| `bulk.return.wizard` | Transient wizard for returning multiple loans in one action |

## Installation

1. Copy the `equipment_loan_tracker` folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Activate developer mode, go to **Apps**, and click **Update Apps List**.
4. Search for "Equipment Loan Tracker" and click **Install**.

To apply changes after pulling updates:

```
odoo -d <your_db> -u equipment_loan_tracker --stop-after-init
```

## Usage

1. Go to **Equipment Loans → Configuration → Equipment** and register your equipment.
2. Go to **Equipment Loans → Loans** and create a loan: choose the employee and equipment, then set either the return date or the duration in days.
3. When the item comes back, click **Mark Returned** on the loan.
4. To return several loans at once, tick them in the list view and use **Bulk Return** (header button or Action menu), pick a return date, and confirm.
5. Assign the **Equipment Manager** group (Settings → Users) to anyone who should manage all loans rather than just their own.

## Notes

- The loan sequence record uses `noupdate="1"`. On an existing database, changes to its prefix must be made in **Settings → Technical → Sequences**, not by editing the XML.
- Bulk Return only works on loans the user is allowed to edit. Regular users are limited to their own loans by the record rule.

## Folder structure

```
equipment_loan_tracker/
├── __init__.py
├── __manifest__.py
├── data/
│   ├── ir_sequence.xml
│   └── equipment_data.xml
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
├── static/
│   └── description/
│       ├── icon.png
│       └── index.html
└── views/
    ├── equipment_item_views.xml
    ├── equipment_loan_views.xml
    ├── equipment_actions.xml
    └── equipment_menus.xml
```

## Requirements

- Odoo 19.0 (uses `models.Constraint` and `<list>` views)
- No external Python dependencies beyond Odoo core

## License

LGPL-3

## Author

Chike Chiagbaizu