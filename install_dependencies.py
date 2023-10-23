import os
import subprocess

class PoetryProjectCreator:
    def __init__(self, project_name, libraries):
        self.project_name = project_name
        self.libraries = libraries

    def create_virtual_environment(self):
        subprocess.run(["python", "-m", "venv", f"{self.project_name}_env"], check=True)
        is_linux = os.name != 'nt'
        command = f"source {self.project_name}_env/bin/activate" \
            if is_linux else f"{self.project_name}_env\\Scripts\\activate"
        subprocess.run([command], shell=True, check=True)
        return self

    def install_poetry(self):
        subprocess.run(["pip", "install", "poetry"], check=True)
        return self

    def create_project(self):
        subprocess.run(["poetry", "new", self.project_name], check=True)
        os.chdir(self.project_name)
        return self

    def add_libraries(self):
        for library in self.libraries:
            subprocess.run(["poetry", "add", library], check=True)
        return self

    def display_dependencies(self):
        subprocess.run(["poetry", "show"], check=True)
        return self

    def deactivate_environment(self):
        deactivate_cmd = "deactivate" if os.name != 'nt' else "deactivate"
        subprocess.run([deactivate_cmd], shell=True, check=True)
        return self

    def create(self):
        if not os.path.exists(self.project_name):
            self.create_virtual_environment() \
                        .install_poetry()\
                        .create_project()\
                        .add_libraries()\
                        .display_dependencies()\
                        .deactivate_environment()
        else:
            print("Project already exists, adding libraries to the environment")
            self.deactivate_environment()
            os.chdir(self.project_name)
            self.add_libraries()\
                .display_dependencies()\
                .deactivate_environment()

if __name__ == "__main__":
    # Define your project name and desired libraries with versions
    PROJECT_NAME = "tbreed" # text-based retrieval on enron email dataset
    LIBRARIES = [
        "scikit-learn==1.3.1",
        "tqdm==4.66.1",
        "pandas==2.1.1"
    ]

    # Create an instance of the PoetryProjectCreator class and run the automation
    creator = PoetryProjectCreator(PROJECT_NAME, LIBRARIES)
    creator.create()
