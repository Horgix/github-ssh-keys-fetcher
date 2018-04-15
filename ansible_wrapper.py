import os
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor import playbook_executor
from ansible.utils.display import Display


# This Ansible Options and Runner structure is inspired by this article:
# https://serversforhackers.com/c/running-ansible-2-programmatically
# The following page has also been helpful:
# http://docs.ansible.com/ansible/latest/dev_guide/developing_api.html

class Options(object):
    """
    Options class to replace Ansible OptParser
    """

    def __init__(self):
        self.verbosity = None
        self.inventory = None
        self.listhosts = None
        self.subset = None
        self.module_paths = None
        self.extra_vars = None
        self.forks = None
        self.ask_vault_pass = None
        self.vault_password_files = None
        self.new_vault_password_file = None
        self.output_file = None
        self.one_line = None
        self.tree = None
        self.ask_sudo_pass = None
        self.ask_su_pass = None
        self.sudo = None
        self.sudo_user = None
        self.become = None
        self.become_method = None
        self.become_user = None
        self.become_ask_pass = None
        self.ask_pass = None
        self.private_key_file = None
        self.remote_user = None
        self.connection = None
        self.timeout = None
        self.ssh_common_args = None
        self.sftp_extra_args = None
        self.scp_extra_args = None
        self.ssh_extra_args = None
        self.poll_interval = None
        self.seconds = None
        self.check = None
        self.syntax = None
        self.diff = None
        self.force_handlers = None
        self.flush_cache = None
        self.listtasks = None
        self.listtags = None
        self.module_path = None


class PlaybookRunner(object):
    def __init__(self, playbook, extra_vars, check_mode=True, verbosity=0):
        self.extra_vars = extra_vars
        self.options = Options()
        self.options.verbosity = verbosity
        self.options.connection = 'local'  # Need a connection type "smart" or "ssh"
        self.options.become = True
        self.options.become_method = 'sudo'
        self.options.become_user = 'root'
        self.options.check = check_mode

        # Set global verbosity
        self.display = Display()
        self.display.verbosity = self.options.verbosity
        # Executor appears to have it's own 
        # verbosity object/setting as well
        playbook_executor.verbosity = self.options.verbosity

        # Gets data from YAML/JSON files
        self.loader = DataLoader()
        # self.loader.set_vault_password(os.environ['VAULT_PASS'])

        # Set inventory, using most of above objects
        self.inventory = InventoryManager(loader=self.loader, sources="localhost,")
        # All the variables from all the various places
        self.variable_manager = VariableManager(loader=self.loader,
                                                inventory=self.inventory)

        self.variable_manager.set_inventory(self.inventory)
        self.variable_manager.extra_vars = self.extra_vars

        # Playbook to run. Assumes it is local to this python file
        pb_dir = os.path.dirname(__file__)
        playbook = "%s/%s" % (pb_dir, playbook)

        # Setup playbook executor, but don't run until run() called
        self.pbex = playbook_executor.PlaybookExecutor(
            playbooks=[playbook],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords={})

    def run(self):
        # Results of PlaybookExecutor
        self.pbex.run()
        # noinspection PyProtectedMember
        stats = self.pbex._tqm._stats

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            if t['unreachable'] > 0 or t['failures'] > 0:
                raise Exception("Had some failure")
