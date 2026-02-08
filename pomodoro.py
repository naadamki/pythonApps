import tkinter as tk
from tkinter import messagebox, ttk
import time


class SettingsDialog:
    def __init__(self, parent, current_settings):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("400x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store current settings
        self.settings = current_settings.copy()
        
        self.setup_ui()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.dialog,
            text="Pomodoro Settings",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=15)
        
        # Settings frame
        settings_frame = tk.Frame(self.dialog)
        settings_frame.pack(pady=10, padx=30, fill="both", expand=True)
        
        # Focus duration
        tk.Label(settings_frame, text="Focus Duration (minutes):", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=10)
        self.focus_var = tk.IntVar(value=self.settings['focus_duration'] // 60)
        focus_spinbox = tk.Spinbox(
            settings_frame,
            from_=1,
            to=120,
            textvariable=self.focus_var,
            width=10,
            font=("Arial", 11)
        )
        focus_spinbox.grid(row=0, column=1, pady=10, padx=10)
        
        # Short break duration
        tk.Label(settings_frame, text="Short Break (minutes):", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=10)
        self.short_break_var = tk.IntVar(value=self.settings['short_break_duration'] // 60)
        short_break_spinbox = tk.Spinbox(
            settings_frame,
            from_=1,
            to=60,
            textvariable=self.short_break_var,
            width=10,
            font=("Arial", 11)
        )
        short_break_spinbox.grid(row=1, column=1, pady=10, padx=10)
        
        # Long break duration
        tk.Label(settings_frame, text="Long Break (minutes):", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=10)
        self.long_break_var = tk.IntVar(value=self.settings['long_break_duration'] // 60)
        long_break_spinbox = tk.Spinbox(
            settings_frame,
            from_=1,
            to=120,
            textvariable=self.long_break_var,
            width=10,
            font=("Arial", 11)
        )
        long_break_spinbox.grid(row=2, column=1, pady=10, padx=10)
        
        # Sessions before long break
        tk.Label(settings_frame, text="Focus sessions before long break:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=10)
        self.sessions_var = tk.IntVar(value=self.settings['sessions_before_long_break'])
        sessions_spinbox = tk.Spinbox(
            settings_frame,
            from_=1,
            to=10,
            textvariable=self.sessions_var,
            width=10,
            font=("Arial", 11)
        )
        sessions_spinbox.grid(row=3, column=1, pady=10, padx=10)
        
        # Auto-start next session
        self.auto_start_var = tk.BooleanVar(value=self.settings.get('auto_start_next', False))
        auto_start_check = tk.Checkbutton(
            settings_frame,
            text="Auto-start next session",
            variable=self.auto_start_var,
            font=("Arial", 11)
        )
        auto_start_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            font=("Arial", 12),
            width=10,
            bg="#4CAF50",
            fg="white",
            command=self.save_settings
        )
        save_btn.grid(row=0, column=0, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 12),
            width=10,
            bg="#757575",
            fg="white",
            command=self.dialog.destroy
        )
        cancel_btn.grid(row=0, column=1, padx=5)
        
    def save_settings(self):
        self.result = {
            'focus_duration': self.focus_var.get() * 60,
            'short_break_duration': self.short_break_var.get() * 60,
            'long_break_duration': self.long_break_var.get() * 60,
            'sessions_before_long_break': self.sessions_var.get(),
            'auto_start_next': self.auto_start_var.get()
        }
        self.dialog.destroy()


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # Timer settings (in seconds)
        self.focus_duration = 25 * 60      # 25 minutes
        self.short_break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 15 * 60  # 15 minutes
        self.auto_start_next = False  # Auto-start next session after timer finishes
        
        # Pomodoro tracking
        self.completed_focus_sessions = 0
        self.sessions_before_long_break = 4  # Standard Pomodoro technique
        
        # Timer state
        self.time_remaining = self.focus_duration
        self.is_focus = True
        self.is_running = False
        self.timer_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top frame with title and settings button
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=15, fill="x", padx=20)
        
        # Settings button (top right)
        settings_btn = tk.Button(
            top_frame,
            text="⚙ Settings",
            font=("Arial", 10),
            bg="#757575",
            fg="white",
            command=self.open_settings
        )
        settings_btn.pack(side="right")
        
        # Mode label
        self.mode_label = tk.Label(
            self.root, 
            text="FOCUS TIME", 
            font=("Arial", 24, "bold"),
            fg="#d32f2f"
        )
        self.mode_label.pack(pady=5)
        
        # Session counter
        self.session_label = tk.Label(
            self.root,
            text="Session 0/4",
            font=("Arial", 12),
            fg="#666"
        )
        self.session_label.pack(pady=5)
        
        # Timer display
        self.time_label = tk.Label(
            self.root, 
            text="25:00", 
            font=("Arial", 48, "bold"),
            fg="#333"
        )
        self.time_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Start/Pause button
        self.start_pause_btn = tk.Button(
            button_frame,
            text="Start",
            font=("Arial", 14),
            width=10,
            bg="#4CAF50",
            fg="white",
            command=self.toggle_timer
        )
        self.start_pause_btn.grid(row=0, column=0, padx=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            font=("Arial", 14),
            width=10,
            bg="#f44336",
            fg="white",
            command=self.stop_timer
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Restart buttons frame
        restart_frame = tk.Frame(self.root)
        restart_frame.pack(pady=10)

        # Restart Focus button
        self.restart_focus_btn = tk.Button(
            restart_frame,
            text="Focus",
            font=("Arial", 12),
            width=15,
            bg="#2196F3",
            fg="white",
            command=self.restart_focus
        )
        self.restart_focus_btn.grid(row=0, column=0, padx=5)
        
        # Restart Break button
        self.restart_break_btn = tk.Button(
            restart_frame,
            text="Short Break",
            font=("Arial", 12),
            width=15,
            bg="#FF9800",
            fg="white",
            command=self.restart_break
        )
        self.restart_break_btn.grid(row=0, column=1, padx=5)



    def open_settings(self):
        # Get current settings
        current_settings = {
            'focus_duration': self.focus_duration,
            'short_break_duration': self.short_break_duration,
            'long_break_duration': self.long_break_duration,
            'sessions_before_long_break': self.sessions_before_long_break,
            'auto_start_next': self.auto_start_next
        }
        
        # Open settings dialog
        dialog = SettingsDialog(self.root, current_settings)
        self.root.wait_window(dialog.dialog)
        
        # Apply new settings if saved
        if dialog.result:
            was_running = self.is_running
            if was_running:
                self.pause_timer()
            
            self.focus_duration = dialog.result['focus_duration']
            self.short_break_duration = dialog.result['short_break_duration']
            self.long_break_duration = dialog.result['long_break_duration']
            self.sessions_before_long_break = dialog.result['sessions_before_long_break']
            self.auto_start_next = dialog.result['auto_start_next']
            
            # Reset current timer to new duration
            if self.is_focus:
                self.time_remaining = self.focus_duration
            else:
                if self.completed_focus_sessions % self.sessions_before_long_break == 0 and self.completed_focus_sessions > 0:
                    self.time_remaining = self.long_break_duration
                else:
                    self.time_remaining = self.short_break_duration
            
            self.update_display()
            
            messagebox.showinfo("Settings Saved", "Settings have been updated!")
        
    def toggle_timer(self):
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
            
    def start_timer(self):
        self.is_running = True
        self.start_pause_btn.config(text="Pause", bg="#FF9800")
        self.countdown()
        
    def pause_timer(self):
        self.is_running = False
        self.start_pause_btn.config(text="Resume", bg="#4CAF50")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
    def stop_timer(self):
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        # Reset to current mode's duration
        if self.is_focus:
            self.time_remaining = self.focus_duration
        else:
            # Determine if it should be short or long break
            if self.completed_focus_sessions % self.sessions_before_long_break == 0 and self.completed_focus_sessions > 0:
                self.time_remaining = self.long_break_duration
            else:
                self.time_remaining = self.short_break_duration
            
        self.update_display()
        self.start_pause_btn.config(text="Start", bg="#4CAF50")
        
    def restart_focus(self):
        self.stop_timer()
        self.is_focus = True
        self.time_remaining = self.focus_duration
        self.mode_label.config(text="FOCUS TIME", fg="#d32f2f")
        self.update_display()
        
    def restart_break(self):
        self.stop_timer()
        self.is_focus = False
        
        # Determine if it should be short or long break
        if self.completed_focus_sessions % self.sessions_before_long_break == 0 and self.completed_focus_sessions > 0:
            self.time_remaining = self.long_break_duration
            self.mode_label.config(text="LONG BREAK", fg="#1976D2")
        else:
            self.time_remaining = self.short_break_duration
            self.mode_label.config(text="SHORT BREAK", fg="#388E3C")
            
        self.update_display()

    def start_focus(self):
        self.stop_timer()
        self.is_focus = True
        self.time_remaining = self.focus_duration
        self.mode_label.config(text="FOCUS TIME", fg="#d32f2f")
        self.update_display()

    def start_short_break(self):
        self.stop_timer()
        self.is_focus = False
        self.time_remaining = self.short_break_duration
        self.mode_label.config(text="SHORT BREAK", fg="#388E3C")
        self.update_display()

    def start_long_break(self):
        self.stop_timer()
        self.is_focus = False
        self.time_remaining = self.long_break_duration
        self.mode_label.config(text="LONG BREAK", fg="#1976D2")
        self.update_display()


    def countdown(self):
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.time_remaining == 0:
            self.timer_finished()
            
    def update_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # Update session counter
        current_session = self.completed_focus_sessions % self.sessions_before_long_break
        self.session_label.config(text=f"Session {current_session}/{self.sessions_before_long_break}")
        
    def timer_finished(self):
        self.is_running = False
        self.start_pause_btn.config(text="Start", bg="#4CAF50")
        
        # Flash the window to get attention
        self.root.bell()
        
        # Show completion message and offer next step
        if self.is_focus:
            # Focus session completed
            self.completed_focus_sessions += 1
            self.update_display()  # Update session counter
            
            # Determine if next break should be long or short
            if self.completed_focus_sessions % self.sessions_before_long_break == 0:
                break_type = "long break"
                message = f"Focus session complete! You've finished {self.sessions_before_long_break} sessions.\n\nTime for a long break (15 minutes)!"
            else:
                break_type = "short break"
                message = f"Focus session complete!\n\nTime for a short break (5 minutes)!"
            
            if self.auto_start_next:
                # Auto-start the break
                messagebox.showinfo("Focus Complete!", message)
                self.restart_break()
                self.start_timer()
            else:
                # Ask user if they want to start break
                result = messagebox.askquestion(
                    "Focus Complete!", 
                    message + "\n\nStart break now?",
                    icon='info'
                )
                
                if result == 'yes':
                    self.restart_break()
                    self.start_timer()
        else:
            # Break completed
            message = "Break complete!\n\nReady to focus again?"
            
            if self.auto_start_next:
                # Auto-start focus session
                messagebox.showinfo("Break Complete!", message.replace("?", "!"))
                self.restart_focus()
                self.start_timer()
            else:
                # Ask user if they want to start focus
                result = messagebox.askquestion(
                    "Break Complete!",
                    message,
                    icon='info'
                )
                
                if result == 'yes':
                    self.restart_focus()
                    self.start_timer()


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()