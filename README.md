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

## Example Usage and Output

```
$ python cfn_validator.py Test/bad_template.yml Test/input_params_bad_template.json


#############################
Validate Parameters Section
#############################


Verify All Template Parameters are Provided by the input_params.json File:
--------------------------------------------------------------------------

Not all Parameters in the template were provided in the input_params.json file. The missing input parameters are:
{'Param2'}


#############################
Validate Resources Section
#############################


Verify All Template Resource Types are Valid:
---------------------------------------------

Not all resources in the template are valid resource types based on the resource specifications for the region. The invalid resources are:
['resource-with-non-valid-type']


Verify All Template Resources have Valid Properties:
----------------------------------------------------

Resource 'resource-with-non-valid-type' has an invalid type: 'AWS::ECS::Services'.  Exiting further checks on this resource

Some resources in the template have invalid properties. The invalid resource properties are:
['resource-with-non-valid-property.TaskDefinitions']


Verify All Template Resources have Required Properties:
-------------------------------------------------------

Resource 'resource-with-non-valid-type' has an invalid type: 'AWS::ECS::Services'.  Exiting further checks on this resource

Required properties have not been specified for some resources in the template. The missing required resource properties are:
['resource-without-required-property.TaskDefinition']

```

```
$ python cfn_validator.py Test/good_template.yml Test/input_params_good_template.json


#############################
Validate Parameters Section
#############################


Verify All Template Parameters are Provided by the input_params.json File:
--------------------------------------------------------------------------

No Issues


#############################
Validate Resources Section
#############################


Verify All Template Resource Types are Valid:
---------------------------------------------

No Issues


Verify All Template Resources have Valid Properties:
----------------------------------------------------

No Issues


Verify All Template Resources have Required Properties:
-------------------------------------------------------

No Issues

```