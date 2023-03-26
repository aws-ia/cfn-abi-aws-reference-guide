from time import sleep
import json
from os import environ
import logging
import cfnresponse

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SESSION = boto3.session.Session()

SH = SESSION.client('securityhub')

def list_products():
    '''
    List all products in Security Hub
    '''
    products = []
    response = SH.describe_products()
    products.extend(response['Products'])
    while 'NextToken' in response:
        response = SH.describe_products(NextToken=response['NextToken'])
        products.extend(response['Products'])
    return products


def query_product_info(filters='ProductArn'):
    '''
    Return a list based on filter keyword
    '''
    products = list_products()
    return [product[filters] for product in products]


def enable_product(product_arn):
    '''
    Enable a product in Security Hub
    '''
    subscription_arn = is_product_enabled(product_arn)
    if subscription_arn:
        LOGGER.warn('Product %s already enabled', product_arn)
    else:
        LOGGER.info('Enabling product %s', product_arn)
        SH.enable_import_findings_for_product(ProductArn=product_arn)

def disable_product(product_arn):
    '''
    Disable a product in Security Hub
    '''
    subscription_arn = is_product_enabled(product_arn)
    if subscription_arn:
        LOGGER.info('Disabling product %s', product_arn)
        SH.disable_import_findings_for_product(ProductSubscriptionArn=subscription_arn)
    else:
        LOGGER.warn('No active subscription found for %s', product_arn)

def list_enabled_products():
    '''
    List all enabled products in Security Hub
    '''
    enabled_products = []
    response = SH.list_enabled_products_for_import()
    enabled_products.extend(response['ProductSubscriptions'])
    while 'NextToken' in response:
        response = SH.list_enabled_products_for_import(NextToken=response['NextToken'])
        enabled_products.extend(response['ProductSubscriptions'])
    return enabled_products

def is_product_enabled(product_arn):
    '''
    Check if a product is enabled in Security Hub
    '''
    partner_name = product_arn.split(':product/')[-1]
    enabled_products = list_enabled_products()
    for product in enabled_products:
        if partner_name in product:
            return product
    return False

def list_partner_integrations(filters='ProductArn'):
    '''
    List all partner integrations in Security Hub
    '''
    integrations = []
    products = list_products()
    for product in products:
        if product['CompanyName'] != 'AWS':
            integrations.append(product[filters])
    return integrations

def handler(event, context):
    '''
    Main function
    '''

    LOGGER.info('Received event: %s', json.dumps(event))
    region = SESSION.region_name
    product_arn = environ['PRODUCT_ARN'].split(':')
    product_arn = ':'.join(product_arn[:3] + [region] + product_arn[4:])
    status = cfnresponse.SUCCESS

    if product_arn in query_product_info():
        try:
            if event['RequestType'] == 'Delete':
                disable_product(product_arn)
            else:
                enable_product(product_arn)
        except Exception as e:
            LOGGER.error('Exception: %s', e, exc_info=True)
            status = cfnresponse.FAILED
    else:
        LOGGER.warn('Invalid ProductArn %s recieved ', product_arn)

    cfnresponse.send(event, context, status, {}, None)