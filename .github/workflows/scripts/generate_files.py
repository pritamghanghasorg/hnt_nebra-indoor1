"""
The script is meant ot be used by github actions and takes the complete repository name
as first and only argument.
eg. python generate_files.py NebraLtd/hnt_rak-v1
"""
import sys
import os
import yaml
from string import Template
from hm_pyhelper.hardware_definitions import variant_definitions

# form base paths
here = os.path.dirname(os.path.abspath(__file__))
templates_folder = os.path.join(here, '../templates')
readme_filename = os.path.join(here, '../../../README.md')
balena_yml_filename = os.path.join(here, '../../../balena.yml')

# extract repository name, variant and vendor name.
REPOSITORY = sys.argv[1].split('/')[1]
VARIANT = REPOSITORY.split('_')[1]
VENDOR = VARIANT.split('-')[0]

# create template dict
variant_defs = variant_definitions[VARIANT]
template_data = {}
template_data['VARIANT_NAME'] = VARIANT
template_data['REPO_NAME'] = REPOSITORY
template_data['VENDOR'] = VENDOR if VENDOR.isupper() else VENDOR.capitalize()
template_data['FLEET'] = f"hnt_{VARIANT}_mainnet_openfleet"
template_data['DEFAULT_DEVICE_NAME'] = variant_defs["BALENA_DEVICE_TYPE"][0]

# update supported models
supported_models_key = 'SUPPORTED_MODELS'
supported_models = [variant_defs['FRIENDLY']]
if supported_models_key in variant_defs.keys():
    supported_models = variant_defs[supported_models_key]
models = ", ".join(supported_models)
template_data['SUPPORTED_MODELS'] = models

# render templates
balena_yml_template = Template(open(os.path.join(templates_folder,
                                                 'balena.yml.template')).read())
readme_template = Template(open(os.path.join(templates_folder,
                                             'README.md.template')).read())
balena_output = balena_yml_template.substitute(template_data)
readme_output = readme_template.substitute(template_data)

# load into yaml and update supported device types and models
balena_yaml = yaml.safe_load(balena_output)
balena_yaml["data"]["supportedDeviceTypes"] = variant_defs["BALENA_DEVICE_TYPE"]

# write out the rendered data.
with open(balena_yml_filename, 'w') as f:
    f.write(yaml.dump(balena_yaml, indent=2, sort_keys=False))

with open(readme_filename, 'w') as f:
    f.write(readme_output)
