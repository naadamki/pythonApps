import customtkinter as ctk

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern To-Do")
        self.geometry("300x400")

        self.entry = ctk.CTkEntry(self, placeholder_text="Add a task...")
        self.entry.pack(pady=20, padx=20, fill="x")

        self.add_button = ctk.CTkButton(self, text="Add", command=self.add_task)
        self.add_button.pack(pady=10)

        self.tasks_list = ctk.CTkScrollableFrame(self)
        self.tasks_list.pack(pady=10, padx=20, fill="both", expand=True)

    def add_task(self):
        task_text = self.entry.get()
        if task_text:
            label = ctk.CTkCheckBox(self.tasks_list, text=task_text)
            label.pack(pady=5, anchor="w")
            self.entry.delete(0, 'end')

app = TodoApp()
app.mainloop()
