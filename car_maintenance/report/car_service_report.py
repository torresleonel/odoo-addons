# -*- coding: utf-8 -*-
"""Defines the models concerning the car maintenance service custom reports."""

from odoo import models


class CarServiceLineReport(models.AbstractModel):
    """Report of service most requested."""

    _name = 'report.car_maintenance.car_service_line_most_requested'
    _description = 'Report of service most requested'

    def _get_report_values(self, docids, data=None):
        services = self.env['car.service.line'].read_group(
            [], ['service_type', 'price'], ['service_type'])
        services.sort(key=lambda s: s.get('service_type_count'), reverse=True)
        service_most_requested = [services.pop(0)] if services else []

        for service in services:
            if service.get('service_type_count') < \
                    service_most_requested[0].get('service_type_count'):
                break
            service_most_requested.append(service)

        return {
            'services': service_most_requested
        }


class CarServiceReport(models.AbstractModel):
    """Report of cars with the highest quantity of services."""

    _name = 'report.car_maintenance.car_service_highest_quantity'
    _description = 'Report for cars with the highest quantity of services'

    def _get_report_values(self, docids, data=None):
        cars_with_services = self.env['car.service'].search(
            [('service_line_ids', '!=', False)])

        return {
            'cars': cars_with_services
        }
