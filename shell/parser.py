from managers.process_manager import ProcessManager
from managers.file_manager import FileManager
from managers.thread_manager import ThreadManager


class CommandParser:
    def execute(self, command_input):

        if command_input.startswith("mkdir"):
            FileManager.mkdir(command_input)
        
        elif command_input.startswith("rmdir -rf"):
            FileManager.remove_recursively(command_input)

        elif command_input.startswith("rmdir"):
            FileManager.rmdir(command_input)

        elif command_input.startswith("cd"):
            FileManager.cd(command_input)
        
        elif command_input.startswith("cp"):
            FileManager.cp(command_input)

        elif command_input.startswith("echo"):
            FileManager.echo(command_input)
        
        elif command_input.startswith("backup-dir"):
            ThreadManager.backup(command_input)
        
        elif command_input.startswith("ls"):
            ProcessManager.execute(command_input)

        elif command_input.startswith("process-test"):
            ProcessManager.test()

        elif command_input.startswith("thread-test"):
            ThreadManager.test()

        else:
            print(f"Unknown command: {command_input}")