from ansible.cli.playbook import PlaybookCLI

mycli = PlaybookCLI

cli = mycli(['-K', 'shell_exam1.yml'])
exit_code = cli.run()
print(exit_code)