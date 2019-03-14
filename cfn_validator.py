from Modules import ValidateTemplate
from Modules import ValidateParameters
from Modules import ValidateResources
import sys

# Globals
region = 'us-west-2'


def get_command_line_arguments_or_exit():
    """
    Get the command line arguments passed to the python script.
    If there are less than 1 or more than 2 arguments passed to the script then
    we will print a help-like output and exit.

    input example:
    python main.py <cfn_template_filename> [input_parameter_filename]

    Returns
        string, string -- filenames for cfn_template and input_params files
    """

    cfn_template_filename = ''
    input_params_filename = ''
    num_arguments_provided = len(sys.argv)

    if num_arguments_provided == 2:
        cfn_template_filename = sys.argv[1]

    if num_arguments_provided == 3:
        cfn_template_filename = sys.argv[1]
        input_params_filename = sys.argv[2]

    if num_arguments_provided < 2 or num_arguments_provided > 3:
        print("usage: python " +
              sys.argv[0] +
              " <cfn_template_filename> [input_parameter_filename]")
        exit()

    return cfn_template_filename, input_params_filename


def print_header(stage):
    """
    Print out the section header
    Should look like this:

    #############################
    {stage}
    #############################

    Arguments:
        stage {string} -- sting to display between header and footer
    """

    header = '#############################'
    print('', '', header, stage, header, sep='\n')


def main():

    cfn_template_filename, input_params_filename = \
        get_command_line_arguments_or_exit()

    template = ValidateTemplate.parse_cfn_template_file(
        cfn_template_filename)

    input_params = ValidateTemplate.parse_input_params_file(
        input_params_filename)

    # Validate Parameters Section
    print_header('Validate Parameters Section')

    ValidateParameters.verify_all_template_params_provided_by_input_params(
        template['Parameters'], input_params)

    # Validate Mappings Section
    # print_header('Validate Mappings Section')

    # Validate Conditions Section
    # print_header('Validate Conditions Section')

    # Validate Resources Section
    print_header('Validate Resources Section')

    resource_specifications = \
        ValidateResources.get_resource_specifications(region)

    ValidateResources.verify_all_template_resource_types_are_valid(
        template, resource_specifications)

    ValidateResources.verify_all_template_resources_have_valid_properties(
        template, resource_specifications)

    ValidateResources.verify_all_template_resources_have_required_properties(
        template, resource_specifications)

    # Validate Outputs Section
    # print_header('Validate Outputs Section')


if __name__ == '__main__':
    main()
