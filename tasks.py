import tkinter as tk
from tkinter import ttk, messagebox


class InfoDialog:
    def __init__(self, parent, current_info):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title('Information')
        self.dialog.geometry('400x400')

        self.setup_ui()

    def setup_ui(self):

        info_frame = tk.Frame(self.dialog)
        info_frame.pack(pady=10, padx=30, fill='both', expand=True)




class Tasks:
    def __init__(self, root):
        self.root = root
        self.root.title('Tasks')
        self.root.geometry('500x500')
        self.root.resizable(False, False)

        self.something_info = 'info about something'

        self.setup_ui()

    
    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=15, fill="x", padx=20)

        info_btn = tk.Button(
            top_frame,
            text='Info',
            bg='#cccccc',
            fg='#ffffff',
            command=self.open_info
        )
        info_btn.pack(side='right')

    def open_info(self):

        current_info = {
            'something': self.something_info
        }

        dialog = InfoDialog(self.root, current_info)
        self.root.wait_window(dialog.dialog)




def main():
    root = tk.Tk()
    app = Tasks(root)
    root.mainloop()


if __name__ == "__main__":
    main()