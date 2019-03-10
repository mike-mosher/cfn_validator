from Modules.awslabs.aws_cfn_template_flip.cfn_tools.yaml_loader import CfnYamlLoader
import yaml
import json


def parse_cfn_template_file(template_filename):
    """
    Take template filename that contains yaml or json data, and return
    json object of the contents

    Note: we are using CfnYamlLoader to parse the files, since the template
    will most likely contain data that is not yaml compliant
    (like Cloudformation shorthand intrinsic functions, ie: "!Ref")

    Arguments:
        template_filename {string} -- filename to open and return contents

    Returns:
        json -- content of the file as json, whether it was yaml or json
        to begin with
    """

    with open(template_filename) as f:
        content = yaml.load(f.read(), Loader=CfnYamlLoader)

    return content


def parse_input_params_file(input_params_filename):
    """
    Take the input_params.json file and parse the contents to json

    We also need to reformat the file before returning:

    input_params.json file that is provided to CloudFormation is in the
    following format:

    [
        {
            "ParameterKey": "RetentionInDays",
            "ParameterValue": "7"
        }
    ]

    This function transforms them into a normal dictionary object in the
    return statement:

    {
        "RetentionInDays": "7"
    }

    Arguments:
        input_params_filename {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    with open(input_params_filename) as f:
        input_params = json.loads(f.read())

    return {param['ParameterKey']: param['ParameterValue']
            for param in input_params}
