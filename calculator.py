import tkinter as tk
from tkinter import ttk
import platform

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        # Variables
        self.current_expression = ""
        self.display_text = tk.StringVar()
        self.display_text.set("0")
        
        # Configure ttk styles
        self.setup_styles()
        
        # Create UI
        self.create_display()
        self.create_buttons()
        
    def setup_styles(self):
        """Configure ttk styles for themed widgets"""
        style = ttk.Style()
        
        # Use native Windows theme
        # On Windows: 'winnative' or 'vista' or 'xpnative'
        # On Mac: 'aqua'
        # On Linux: 'clam' or 'alt'
        
        available_themes = style.theme_names()
        print(f"Available themes: {available_themes}")
        
        # Try to use the most native theme for each platform
        if platform.system() == 'Windows':
            if 'vista' in available_themes:
                style.theme_use('vista')
            elif 'winnative' in available_themes:
                style.theme_use('winnative')
            elif 'xpnative' in available_themes:
                style.theme_use('xpnative')
        elif platform.system() == 'Darwin':  # Mac
            if 'aqua' in available_themes:
                style.theme_use('aqua')
        else:  # Linux
            style.theme_use('clam')
        
        print(f"Using theme: {style.theme_use()}")
        
        # Configure display label style
        style.configure(
            'Display.TLabel',
            background='#1e1e1e',
            foreground='#ffffff',
            font=('Segoe UI', 36, 'bold'),
            padding=20
        )
        
        # Configure number button style
        style.configure(
            'Number.TButton',
            font=('Segoe UI', 18, 'bold'),
            padding=10
        )
        
        # Configure operator button style
        style.configure(
            'Operator.TButton',
            font=('Segoe UI', 18, 'bold'),
            padding=10
        )
        
        # Configure function button style (C, ⌫, %)
        style.configure(
            'Function.TButton',
            font=('Segoe UI', 18, 'bold'),
            padding=10
        )
        
    def create_display(self):
        """Create the calculator display"""
        # Frame for display
        display_frame = ttk.Frame(self.root)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Configure frame background
        style = ttk.Style()
        style.configure('Display.TFrame', background='#1e1e1e')
        
        # Main display using ttk.Label
        display = ttk.Label(
            display_frame,
            textvariable=self.display_text,
            style='Display.TLabel',
            anchor="e"
        )
        display.pack(expand=True, fill="both")
        
    def create_buttons(self):
        """Create calculator buttons"""
        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        
        # Button layout
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                # Determine button style
                if button_text in ['C', '⌫', '%']:
                    btn_style = 'Function.TButton'
                elif button_text in ['/', '*', '-', '+', '=']:
                    btn_style = 'Operator.TButton'
                else:
                    btn_style = 'Number.TButton'
                
                btn = ttk.Button(
                    button_frame,
                    text=button_text,
                    style=btn_style,
                    command=lambda x=button_text: self.on_button_click(x)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
        
        # Configure grid weights for responsive sizing
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.columnconfigure(j, weight=1)
    
    def on_button_click(self, button_text):
        """Handle button clicks"""
        if button_text == 'C':
            self.clear()
        elif button_text == '⌫':
            self.backspace()
        elif button_text == '=':
            self.calculate()
        elif button_text == '±':
            self.toggle_sign()
        else:
            self.append_to_expression(button_text)
    
    def clear(self):
        """Clear the display"""
        self.current_expression = ""
        self.display_text.set("0")
    
    def backspace(self):
        """Remove last character"""
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.display_text.set(self.current_expression if self.current_expression else "0")
    
    def append_to_expression(self, char):
        """Add character to expression"""
        # Prevent multiple operators in a row
        if char in ['+', '-', '*', '/', '%', '.']:
            if self.current_expression and self.current_expression[-1] in ['+', '-', '*', '/', '%', '.']:
                return
        
        # Start fresh if display shows "0" or an error
        if self.current_expression == "" or self.display_text.get() == "Error":
            if char not in ['+', '-', '*', '/', '%']:
                self.current_expression = char
            else:
                return
        else:
            self.current_expression += char
        
        self.display_text.set(self.current_expression)
    
    def calculate(self):
        """Evaluate the expression"""
        try:
            # Replace % with /100 for percentage calculation
            expression = self.current_expression.replace('%', '/100')
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.current_expression = str(result)
            self.display_text.set(self.current_expression)
        except:
            self.display_text.set("Error")
            self.current_expression = ""
    
    def toggle_sign(self):
        """Toggle positive/negative"""
        if self.current_expression and self.current_expression != "0":
            if self.current_expression[0] == '-':
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = '-' + self.current_expression
            self.display_text.set(self.current_expression)

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
