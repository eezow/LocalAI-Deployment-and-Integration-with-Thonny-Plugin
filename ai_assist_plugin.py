import sys
import os
import requests
from thonny import get_workbench
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showerror

# LocalAI API URL
LOCALAI_URL = "http://localhost:8080/v1/completions"

# Function to interact with LocalAI
def query_localai(prompt, model="llama-3-8b-instruct-coder"):
    try:
        response = requests.post(
            LOCALAI_URL,
            json={
                "model": model,
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 300,
            },
            timeout=1000
        )
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("text", "No response from LocalAI.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LocalAI: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Command to send a custom prompt to LocalAI
def ai_code_assist():
    try:
        prompt = simpledialog.askstring(
            "AI Code Assistant",
            "Enter your prompt for LocalAI:",
            parent=get_workbench().winfo_toplevel()
        )
        
        if not prompt:
            showinfo("AI Code Assistant", "Prompt was canceled or empty.")
            return
        
        result = query_localai(prompt)
        showinfo("AI Code Assistant", result)
    except Exception as e:
        showerror("AI Code Assistant", f"An error occurred: {e}")

# Add a menu item in Thonny
def load_plugin():
    try:
        workbench = get_workbench()
        if workbench:
            workbench.add_command(
                command_id="ai_code_assist",
                menu_name="tools",  # Ensure menu name matches Thonny's Tools menu
                command_label="AI Code Assistant",
                handler=ai_code_assist
            )
            print("AI Code Assistant command added successfully!")
        else:
            print("Error: Could not get Thonny workbench.")
    except Exception as e:
        print(f"Error while adding AI Code Assistant command: {e}")

