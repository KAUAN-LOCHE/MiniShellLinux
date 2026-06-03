import os
import shutil
import threading

class ThreadManager:

    @staticmethod
    def backup_dir(dir):

        backup_dir = dir + "_backup"

        os.makedirs(backup_dir, exist_ok = True)


        for item in os.listdir(dir):
            source = os.path.join(dir, item)

            if os.path.isfile(source):
                shutil.copy2(source, backup_dir)

        print(f"Backup completed: {backup_dir}")

    @staticmethod
    def backup(command_input):
        dir = command_input.split()[1]

        thread = threading.Thread(
            target=ThreadManager.backup_dir,
            args=(dir,)
        )

        thread.start()

        print(f"Backup started for directory: {dir}")

    @staticmethod
    def test():
        print("Starting thread test to demonstrate thread management")
        def worker():
            import time
            # time.sleep(2)
            print("Worker thread is exiting")

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()