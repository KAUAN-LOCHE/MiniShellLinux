from shell.parser import CommandParser
import time
class MiniShell:

    def __init__(self):
        self.parser = CommandParser()

    def run(self):
        while True:
            try:
                command_input = input("mini-shell> ").strip()

                if not command_input:
                    continue

                if command_input == "exit":
                    print("Exiting mini-shell.")
                    break

                if command_input.startswith("time"):
                    command_input = command_input[5:] 
                    start_time = time.perf_counter()
                    self.parser.execute(command_input)
                    end_time = time.perf_counter()
                    print(f"Execution time: {end_time - start_time:.6f} seconds")
                else:
                    self.parser.execute(command_input)

            except Exception as e:
                print(f"Error: {e}")