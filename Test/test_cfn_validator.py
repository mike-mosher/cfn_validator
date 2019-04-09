"""Tests for cfn_validator.py"""

import pytest
from cfn_validator import ValidateParameters


def test_verify_all_template_params_provided_by_input_params():
    template_params = {}
    input_params = None
    no_input_params_error_msg = '\'input_parameter_filename\' not provided.  Exiting.'

    assert ValidateParameters.verify_all_template_params_provided_by_input_params(
        template_params=template_params, input_params=input_params) == no_input_params_error_msg
