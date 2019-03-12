import json
import requests
from collections import defaultdict

# Globals
resource_specifications_url_by_region = {
    'ap-south-1': 'https://d2senuesg1djtx.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ap-northeast-3': 'https://d2zq80gdmjim8k.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ap-northeast-2': 'https://d1ane3fvebulky.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ap-southeast-1': 'https://doigdx0kgq9el.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ap-southeast-2': 'https://d2stg8d246z9di.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ap-northeast-1': 'https://d33vqc0rt9ld30.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'ca-central-1': 'https://d2s8ygphhesbe7.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'eu-central-1': 'https://d1mta8qj7i28i2.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'eu-west-1': 'https://d3teyb21fexa9r.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'eu-west-2': 'https://d1742qcu2c1ncx.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'eu-west-3': 'https://d2d0mfegowb3wk.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'eu-north-1': 'https://diy8iv58sj6ba.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'sa-east-1': 'https://d3c9jyj3w509b0.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'us-east-1': 'https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'us-east-2': 'https://dnwj8swjjbsbt.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'us-west-1': 'https://d68hl49wbnanq.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json',
    'us-west-2': 'https://d201a2mn26r7lk.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json'
}


def print_header(msg):
    """
    Print out the section header
    Should look like this:

    Verify All Template Resource Types are Valid:
    --------------------------------------------

    Arguments:
        msg {string} -- sting to display
    """

    msg = msg + ':'
    underline = '-' * len(msg)
    print('', '', msg, underline, '', sep='\n')


def get_resource_specifications(region):
    """
    The AWS CloudFormation resource specification is a JSON-formatted text
    file that defines the resources and properties that AWS CloudFormation
    supports. The document is a machine-readable, strongly typed specification
    that you can use to build tools for creating AWS CloudFormation templates.
    For example, you can use the specification to build auto completion and
    validation functionality for AWS CloudFormation templates in your
    IDE (integrated development environment).

    Description URL: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html

    Returns
        dict -- full resource specifications json data
    """

    return requests.get(resource_specifications_url_by_region[region]).json()


def verify_all_template_resource_types_are_valid(
        template, resource_specifications):
    """
    Verify the template resources against the resource specifications that
    CloudFormation defines for the region

    Return any non-valid resources found in the template

    Arguments:
        template {dict} -- CloudFormation template
        resource_specifications {dict} -- Resource Specification json object
    """

    print_header('Verify All Template Resource Types are Valid')

    non_valid_template_resources = []

    for resource_name, resource in template['Resources'].items():
        if resource['Type'] not in \
                resource_specifications['ResourceTypes'].keys():
            non_valid_template_resources.append(resource_name)

    if non_valid_template_resources:
        print('Not all resources in the template are valid resource types '
              'based on the resource specifications for the region. The '
              'invalid resources are:')
        print(non_valid_template_resources)
    else:
        print('No Issues')


def verify_all_template_resources_have_valid_properties(
        template, resource_specifications):
    """
    Verify the properties of the template resources against the resource
    specifications that CloudFormation defines for the region.

    Print error for any non-valid resource properties found

    Arguments:
        template {dict} -- CloudFormation template
        resource_specifications {dict} -- Resource Specification json object
    """

    print_header('Verify All Template Resources have Valid Properties')

    template_resources_with_non_valid_properties = []

    for resource_name, resource in template['Resources'].items():

        try:
            spec_resource_properties = \
                resource_specifications[
                    'ResourceTypes'][resource['Type']]['Properties'].keys()
        except KeyError as e:
            # We are here because we tried to find the template resource type
            # in the resource specification and we received a KeyError
            # meaning that the resource type is not valid
            print('Resource \'' + resource_name + '\' '
                    'has an invalid type: \'' + resource['Type'] + '\'.  '
                    'Exiting further checks on this resource', '', sep='\n')
            continue

        for property_name, property in resource['Properties'].items():
            if property_name not in spec_resource_properties:
                # String: AWS::EC2::Instance.ImageId
                resource_property_identifier = \
                    resource_name + '.' + property_name
                template_resources_with_non_valid_properties.append(
                    resource_property_identifier)

    if template_resources_with_non_valid_properties:
        print('Some resources in the template have invalid properties. The '
              'invalid resource properties are:')
        print(template_resources_with_non_valid_properties)
    else:
        print('No Issues')


def verify_all_template_resources_have_required_properties(
        template, resource_specifications):
    """
    Verify that template resources have all required properties based on
    the resource specifications that CloudFormation defines for the region.

    Print error for any missing required resource properties found

    Arguments:
        template {dict} -- CloudFormation template
        resource_specifications {dict} -- Resource Specification json object
    """
    print_header('Verify All Template Resources have Required Properties')

    required_resource_properties_missing_from_template = []

    for resource_name, resource in template['Resources'].items():

        template_resource_properties = resource['Properties'].keys()

        try:
            spec_resource_properties = resource_specifications[
                'ResourceTypes'][resource['Type']]['Properties']
        except KeyError as e:
            # We are here because we tried to find the template resource type
            # in the resource specification and we received a KeyError
            # meaning that the resource type is not valid
            print('Resource \'' + resource_name + '\' '
                    'has an invalid type: \'' + resource['Type'] + '\'.  '
                    'Exiting further checks on this resource', '', sep='\n')
            continue

        spec_resource_required_properties = []
        for property_name, property in spec_resource_properties.items():
            if property['Required']:
                spec_resource_required_properties.append(property_name)

        for required_property in spec_resource_required_properties:
            if required_property not in template_resource_properties:
                # String: AWS::EC2::Instance.ImageId
                resource_property_identifier = \
                    resource_name + '.' + required_property

                required_resource_properties_missing_from_template.append(
                    resource_property_identifier)

    if required_resource_properties_missing_from_template:
        print('Required properties have not been specified for some resources '
              'in the template. The missing required resource properties are:')
        print(required_resource_properties_missing_from_template)
    else:
        print('No Issues')
