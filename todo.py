import json
import os

class Task:
    def __init__(self, title, description=None, category=None, project=None, urgent=False, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.project = project
        self.urgent = urgent
        self.completed = completed

    def to_dict(self):
        return self.__dict__

    def update_title(self, new_title):
        self.title = new_title    

    def update_description(self, new_description):
        self.description = new_description

    def update_category(self, new_category):
        self.category = new_category

    def update_project(self, new_project):
        self.project = new_project

    def toggle_urgent(self):
        self.urgent = not self.urgent

    def toggle_completed(self):
        self.completed = not self.completed


class Manager:
    def __init__(self, filename='todo.json'):
        self.filename = filename
        self._set_defaults()
        self.load_data()

    def _set_defaults(self):
        """Initializes empty state for the manager."""
        self.tasks = {}
        self.projects = ['General']
        self.categories = []

    def load_data(self):
        if not os.path.exists(self.filename):
            self.save_data()
            return

        try:
            with open(self.filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    raise json.JSONDecodeError("Empty file", "", 0)
                
                data = json.loads(content)
                
                # Reconstruct Task objects
                self.tasks = {
                    title: Task(**details) 
                    for title, details in data.get('tasks', {}).items()
                }
                self.projects = data.get('projects', ['General'])
                self.categories = data.get('categories', [])

        except (json.JSONDecodeError, TypeError, KeyError):
            # If invalid, rename to backup and start fresh
            backup_name = f"{self.filename.replace('.json', '')}_backup.json"
            print(f"Invalid JSON detected. Renaming {self.filename} to {backup_name}")
            
            if os.path.exists(self.filename):
                os.rename(self.filename, backup_name)
            
            self._set_defaults()
            self.save_data()

    def save_data(self):
        output = {
            "tasks": {title: task.to_dict() for title, task in self.tasks.items()},
            "projects": self.projects,
            "categories": self.categories
        }
        with open(self.filename, 'w') as f:
            json.dump(output, f, indent=4)
        
    def delete_project(self, project_name, delete_tasks=False):
        """
        Removes a project. 
        If delete_tasks is True, it removes all associated tasks.
        If False, it moves tasks to 'General'.
        """
        if project_name not in self.projects:
            print(f"Project '{project_name}' not found.")
            return

        if project_name == 'General':
            print("Cannot delete the 'General' project.")
            return

        # Remove the project from the master list
        self.projects.remove(project_name)

        if delete_tasks:
            # Comprehension: Keep only tasks NOT in the deleted project
            self.tasks = {
                title: task for title, task in self.tasks.items() 
                if task.project_name != project_name
            }
            print(f"Deleted project '{project_name}' and all its tasks.")
        else:
            # Reassign tasks to 'General' instead of deleting them
            for task in self.tasks.values():
                if task.project_name == project_name:
                    task.project_name = 'General'
            print(f"Deleted project '{project_name}'. Tasks moved to 'General'.")

        self.save_data()

    def add_task(self, title, description=None, category=None, project="General"):
        new_task = Task(title, description=description, category=category, project=project)
        self.tasks[title] = new_task
        
        # Ensure project/category exists in our master lists
        if project not in self.projects: self.projects.append(project)
        if category and category not in self.categories: self.categories.append(category)
        self.save_data()

    def edit_task(self, title, description=None, category=None, project=None):
        if title not in self.tasks:
            print(f"Task '{title}' not found.")
            return

        task = self.tasks[title]

        if description is not None:
            task.update_description(description)
        
        if category is not None:
            task.update_category(category)
            if category not in self.categories:
                self.categories.append(category)

        if project is not None:
            task.update_project(project)
            if project not in self.projects:
                self.projects.append(project)

        self.save_data()
        print(f"Task '{title}' updated successfully.")

    def toggle_task_urgency(self, title):
        if title in self.tasks:
            self.tasks[title].toggle_urgent()
            self.save_data()
            print(f"Urgency updated for '{title}'.")
        else:
            print("Task not found.")

    def toggle_task_status(self, title):
        if title in self.tasks:
            self.tasks[title].toggle_completed()
            self.save_data()
            print(f"Status updated for '{title}'.")
        else:
            print("Task not found.")

    def rename_task(self, old_title, new_title):
        """Handles the complex dictionary key swap."""
        if old_title not in self.tasks:
            print(f"Error: '{old_title}' does not exist.")
            return
        
        if new_title in self.tasks:
            print(f"Error: A task named '{new_title}' already exists.")
            return

        # 1. Pop the task object out of the dict (removes old key)
        task_obj = self.tasks.pop(old_title)
        
        # 2. Update the internal attribute of the Task object
        task_obj.update_title(new_title)
        
        # 3. Put it back in with the new key
        self.tasks[new_title] = task_obj
        
        self.save_data()
        print(f"Renamed '{old_title}' to '{new_title}'.")

    def delete_task(self, title):
        """Removes a task from the dictionary and updates the file."""
        if title in self.tasks:
            del self.tasks[title]
            self.save_data()
            print(f"Task '{title}' deleted.")
        else:
            print(f"Task '{title}' not found.")






if __name__ == "__main__":
    main()
