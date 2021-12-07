# -*- coding: utf-8 -*-
"""Define test cases on access rights for the car maintenance module."""

from odoo.exceptions import AccessError
from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestAccessRights(TransactionCase):
    """Test access rights."""

    @classmethod
    def setUpClass(cls):
        """Set up data for all test cases."""
        super().setUpClass()

        # Avoid sending reset password email: no_reset_password
        users = cls.env['res.users'].with_context(no_reset_password=True)
        cls.operator_user = users.create({
            'name': 'Test Operator User',
            'login': 'test_operator_user',
            'email': 'test_operator_user@example.com',
            'groups_id': [
                Command.set(cls.env.ref('car_maintenance.group_operator').ids)
            ]
        })
        cls.manager_user = users.create({
            'name': 'Test Manager User',
            'login': 'test_manager_user',
            'email': 'test_manager_user@example.com',
            'groups_id': [
                Command.set(cls.env.ref('car_maintenance.group_manager').ids)
            ]
        })

        cls.car_service = cls.env['car.service'].create({
            'license_plate': 'Test License Plate',
            'owner_name': 'Test Owner Name',
            'owner_last_name': 'Test Owner Last Name',
            'service_line_ids': [
                Command.create({'service_type': 'Spark plugs', 'price': 10.0})
            ]
        })

    def test_01_access_operator(self):
        """Test Operator's access rights."""
        cs_operator_user = self.car_service.with_user(self.operator_user)

        # Operator can read, write, create car.service and car.service.line
        cs_operator_user.read()

        cs_operator_user.write({
            'service_line_ids': [
                Command.create({'service_type': 'Coolant', 'price': 20.0})
            ]
        })
        cs_operator_user.service_line_ids[0].update({
            'service_type': 'Clutch', 'price': 45.0
        })

        self.env['car.service'].with_user(self.operator_user).create({
            'license_plate': 'Test License Plate 2',
            'owner_name': 'Test Owner Name 2',
            'owner_last_name': 'Test Owner Last Name 2',
            'service_line_ids': [
                Command.create({'service_type': 'Spark plugs', 'price': 10.0})
            ]
        })

        # Operator can't delete car.service and car.service.line
        with self.assertRaises(AccessError):
            cs_operator_user.service_line_ids.unlink()
            cs_operator_user.unlink()

    def test_02_access_manager(self):
        """Test Manager's access rights."""
        cs_manager_user = self.car_service.with_user(self.manager_user)

        # Manager can do all actions on car.service and car.service.line
        cs_manager_user.read()

        cs_manager_user.write({
            'service_line_ids': [
                Command.create({'service_type': 'Clutch', 'price': 30.0})
            ]
        })
        cs_manager_user.service_line_ids[0].update({
            'service_type': 'Clutch', 'price': 45.0
        })

        self.env['car.service'].with_user(self.manager_user).create({
            'license_plate': 'Test License Plate 3',
            'owner_name': 'Test Owner Name 3',
            'owner_last_name': 'Test Owner Last Name 3',
            'service_line_ids': [
                Command.create({'service_type': 'Spark plugs', 'price': 10.0})
            ]
        })

        cs_manager_user.service_line_ids.unlink()
        cs_manager_user.unlink()
