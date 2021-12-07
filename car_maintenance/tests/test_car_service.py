# -*- coding: utf-8 -*-
"""Define test cases on service for the car maintenance module."""

from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestCarService(TransactionCase):
    """Test car service."""

    @classmethod
    def setUpClass(cls):
        """Set up data for all test cases."""
        super().setUpClass()

        cls.car_service = cls.env['car.service']
        cls.service_line = cls.env['car.service.line']
        cls.car_service_data = {
            'license_plate': 'Test License Plate Unique',
            'owner_name': 'Test Owner Name',
            'owner_last_name': 'Test Owner Last Name'
        }

    @mute_logger('odoo.sql_db')
    def test_01_car_service_unique_license_plate(self):
        """Test license plate must be unique."""
        self.car_service.create(self.car_service_data)
        message = 'license_plate field must be unique'
        with self.assertRaises(IntegrityError, msg=message):
            self.car_service.create(self.car_service_data)

    @mute_logger('odoo.sql_db')
    def test_02_car_service_required_field(self):
        """Test car service required fields."""
        message = 'license_plate field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.car_service.create({
                'owner_name': 'Test Owner Name',
                'owner_last_name': 'Test Owner Last Name'
            })

        message = 'owner_name field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.car_service.create({
                'license_plate': 'Test License Plate 1',
                'owner_last_name': 'Test Owner Last Name'
            })

        message = 'owner_last_name field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.car_service.create({
                'license_plate': 'Test License Plate 2',
                'owner_name': 'Test Owner Name'
            })

    def test_03_service_line_get_name(self):
        """Test the format of the record display name."""
        car = self.car_service.create(self.car_service_data)
        service = self.service_line.create({
            'car_service_id': car.id,
            'price': 10.0,
            'service_type': 'Spark plugs'   
        })

        # Expected format: 'license_plate - service_type'
        self.assertEqual(
            service.name_get()[0][1],
            'Test License Plate Unique - Spark plugs'
        )

    @mute_logger('odoo.sql_db')
    def test_04_service_line_required_field(self):
        """Test car service line required fields."""
        car = self.car_service.create(self.car_service_data)

        message = 'car_service_id field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.service_line.create({
                'price': 10.0,
                'service_type': 'Spark plugs'
            })

        message = 'price field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.service_line.create({
                'car_service_id': car.id,
                'service_type': 'Spark plugs'
            })

        message = 'service_type field must be required'
        with self.assertRaises(IntegrityError, msg=message):
            self.service_line.create({
                'car_service_id': car.id,
                'price': 10.0
            })
