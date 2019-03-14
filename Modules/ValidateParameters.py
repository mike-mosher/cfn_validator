
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


def verify_all_template_params_provided_by_input_params(
        template_params, input_params):
    """
    Validate that all input parameters in the CloudFormation template
    are specified in the input_params.json file

    Note: It is fine if the input_params.json file provides *more*
    parameters that are defined in the template, but it is *not* fine
    if it defines *less* parameters

    if input_params_filename not provided to the script, we will skip this
    test and exit function

    Arguments:
        template_params {dict} -- CloudFormation template dict
        input_params {dict} -- input_params.json dict
    """

    print_header('Verify All Template Parameters are Provided by the '
                 'input_params.json File')

    if not input_params:
        print('\'input_parameter_filename\' not provided.  Exiting.')
        return

    # Subtracting the input params from the template params
    # will give an empty set if the input params
    # are >= to template params
    #
    # if input params <= template params, then there will be
    # items in the set, and the following var will be True
    template_params_not_provided_by_input_params = \
        (template_params.keys() - input_params.keys())

    if template_params_not_provided_by_input_params:
        print('Not all Parameters in the template were provided in the '
              'input_params.json file. The missing input parameters are:')
        print(template_params_not_provided_by_input_params)
    else:
        print('No Issues')
