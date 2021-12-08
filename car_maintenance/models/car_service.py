# -*- coding: utf-8 -*-
"""Defines the models concerning the car maintenance service."""

from odoo import api, fields, models


class CarService(models.Model):
    """Car services model."""

    _name = 'car.service'
    _description = 'Car Services'
    _inherit = ['mail.thread']
    _rec_name = 'license_plate'
    _order = 'service_quantity desc'

    license_plate = fields.Char(help='Car license plate', required=True)
    owner_last_name = fields.Char(help='Car owners last name', required=True)
    owner_name = fields.Char(help='Car owners name', required=True)
    service_line_ids = fields.One2many(
        comodel_name='car.service.line',
        inverse_name='car_service_id',
        help='Services performed on the car'
    )
    service_quantity = fields.Integer(
        help='Quantity of services performed on the car',
        compute='_compute_service_quantity',
        store=True
    )

    _sql_constraints = [(
        'license_plate_key',
        'UNIQUE (license_plate)',
        'You can not have two cars with the same license plate!'
    )]

    @api.depends('service_line_ids')
    def _compute_service_quantity(self):
        for car in self:
            car.service_quantity = len(car.service_line_ids)


class CarServiceLine(models.Model):
    """Model for services performed on cars."""

    _name = 'car.service.line'
    _description = 'Services performed on cars'

    car_service_id = fields.Many2one(
        string='Car',
        help='Car to be serviced',
        comodel_name='car.service',
        required=True
    )
    price = fields.Float(
        help='Price for the service',
        digits='Product Price',
        required=True
    )
    service_type = fields.Selection(
        selection=[
            ('Spark plugs', 'Spark plugs replacement'),
            ('Oil and filter', 'Oil and filter replacement'),
            ('Fuel and air filter', 'Fuel and air filter replacement'),
            ('Coolant', 'Coolant replacement'),
            ('Alternator belt', 'Alternator belt replacement'),
            ('Ignition timing', 'Adjustment of the ignition timing'),
            ('Lights and headlights', 'Revision of lights and headlights'),
            ('Clutch', 'Adjustment of the clutch'),
            (
                'Box, battery, hydraulic levels',
                'Box, battery and hydraulic levels revision'
            ),
            ('Battery terminals', 'Cleaning of battery terminals'),
            ('Brakes and front axle', 'Revision of brakes and front axle')
        ],
        help='Types of services available',
        required=True
    )

    def name_get(self):
        """Define the name of the record visible on the view."""
        result = []
        for service in self:
            name = '{} - {}'.format(
                service.car_service_id.license_plate, service.service_type)
            result.append((service.id, name))
        return result
