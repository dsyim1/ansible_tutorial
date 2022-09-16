import json
import shutil

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible import context



def ansible_task(playbooks):
    Options = namedtuple('Options', \
    ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])

    options = Options(
        connection = 'ssh', 
        module_path = '/opt/ansible/modules',
        forks = 100, 
        become = True, 
        become_method = 'sudo', 
        become_user = 'root', 
        check = False, 
        listhosts = None,
        listtasks = None,
        listtags = None,
        syntax = None
    )

    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/opt/ansible/inventory')
    variable_manager.set_inventory(inventory)

    pb = PlaybookExecutor(playbooks=[playbooks], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=None)
    pb.run()

    stats = pb._tqm._stats
    ips = stats.processed.keys()
    return [ {ip : stats.summarize(ip)} for ip in ips ]