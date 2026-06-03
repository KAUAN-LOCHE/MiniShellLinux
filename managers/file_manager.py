import os
import shutil

class FileManager:

    @staticmethod
    def mkdir(command_input):

        name = command_input.split()[1]
        os.mkdir(name)

    @staticmethod
    def rmdir(command_input):

        name = command_input.split()[1]
        os.rmdir(name)

    @staticmethod
    def remove_recursively(command_input):
        dir = command_input.split()[2]
        shutil.rmtree(dir)

    @staticmethod
    def cd(command_input):

        dir = command_input.split()[1]
        os.chdir(dir)

    @staticmethod
    def cp(command_input):
        _, source, destination = command_input.split()
        shutil.copy2(source, destination)

    @staticmethod
    def echo(command_input):
        content, file = command_input.split(">")

        text = content.replace("echo", "").strip().replace('"', '')

        with open(file.strip(),"w") as f:
            f.write(text)
