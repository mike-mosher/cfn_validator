# CloudFormation Template Validator

## Description

Check the validity of an AWS CloudFormation template.

Currently checked items:

<ins>Parameters Section</ins>:

- Do the parameters defined in the input_params.json file cover the Parameters defined in the template?


<ins>Resources Section</ins>:


- Are all template resource types valid CloudFormation resources?
- Are all resource properties defined in the template valid properties for that resource type?
- Are all required properties for each resource specified in the template?

## Usage

```
usage: python cfn_validator.py <cfn_template_filename> <input_parameter_filename>
```

- _cfn_template_filename_: can be any valid CloudFormation template, either json or yaml
- _input_parameter_filename_: the input parameter file, used to pass parametrs to the [`create-stack`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack.html) or [`update-stack`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/update-stack.html) aws cli commands. This file should contain all parameters specified in the template, and is in the following format:

``` 
[
  {
    "ParameterKey": "string",
    "ParameterValue": "string",
    "UsePreviousValue": true|false,
    "ResolvedValue": "string"
  }
  ...
]
```