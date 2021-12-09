# -*- coding: utf-8 -*-
{
    'name': 'Car maintenance',
    'summary': 'Car maintenance services.',
    'description': """
        It contains some elementary functions to manage the car maintenance.

        Note: developed for job interview.
    """,
    'author': 'Leonel Torres',
    'website': 'https://github.com/torresleonel/odoo-addons',
    'category': 'Services',
    'version': '15.0.0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/car_maintenance_security.xml',
        'security/ir.model.access.csv',
        'views/car_service_views.xml',
        'report/car_service_templates.xml',
        'report/car_service_reports.xml'
    ],
    'demo': ['demo/car_maintenance_demo.xml'],
    'application': True,
    'license': 'LGPL-3'
}
