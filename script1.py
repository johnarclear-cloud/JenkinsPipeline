from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file=config_file)

def load_vars(task):
    host_data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["vars"] = host_data.result

def generate_config(task):
    ospf_template = task.run(task=template_file, template="ospf.j2", path="./templates")
    ospf_result = ospf_template.result
    ospf_config = ospf_result.splitlines()
    task.run(task=netmiko_send_config, config_command=ospf_config)

juniper_nr = nr.filter(platform="juniper_junos")
load_results = juniper_nr.run(task=load_vars)
config_results = juniper_nr(task=generate_config)
print_result(load_results)
print_result(config_results