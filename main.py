"""
This is a simple Python script using the Cisco Meraki library to return the statuses of all devices in an
organization.

Authored by Brian Buxton
"""

import meraki
import csv

API_KEY = ''
dashboard = meraki.DashboardAPI(API_KEY)
organizations = dashboard.organizations.getOrganizations()


def get_devices_status(organization):
    """
    This is a simple function that returns the list of device statuses for an organization.  This function can be
    extended to include any transformations or formatting required in the future.

    :rtype: list
    """
    return dashboard.organizations.getOrganizationDevicesStatuses(organizationId=organization, total_pages='all')


if __name__ == '__main__':
    status_list: list
    status_list = [{'name': serial['name'], 'serial': serial['serial'], 'status': serial['status']} for serial in
                   get_devices_status(organizations[0]['id']) if serial['status'] != 'online' and
                   serial['productType'] == 'camera']
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'serial', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in status_list:
            writer.writerow(row)
