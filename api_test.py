from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import sys
import datetime

loader = DataLoader()
context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                    module_path=None, forks=100, remote_user='yimds', private_key_file='/home/yimds/.ssh/ansible',
                    ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                    become_method='sudo', become_user='root', verbosity=True, check=False, start_at_task=None)

inventory = InventoryManager(loader=loader, sources=('inventory',))

variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))
pbex = PlaybookExecutor(playbooks=['shell_exam1.yml'],  inventory=inventory, variable_manager=variable_manager, loader=loader, passwords={})

op =sys.stdout
date_obj = datetime.datetime.now()
filename='./'+ date_obj.strftime('%Y%m%d%H%M%S')+'.log'
opf=open(filename,'w')
sys.stdout=opf
pbex._tqm._stdout_callback = cb
results = pbex.run()
sys.stdout=op
opf.close
print (open(filename,'r').read())