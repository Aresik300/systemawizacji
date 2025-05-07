import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess

# Zaszyta baza danych
data = {
    "Magazyn A": ["email1@example.com", "email2@example.com"],
    "Magazyn B": ["email3@example.com", "email4@example.com"]
}

class App:
    def __init__(self, root, is_admin=False):
        self.root = root
        self.is_admin = is_admin
        self.data = data
        self.root.title("System Awizacji")
        self.draw_interface()

    def draw_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Wybierz lokalizację:", font=("Arial", 14)).pack(pady=10)

        for location in list(self.data.keys()):
            frame = tk.Frame(self.root)
            frame.pack(pady=3)

            tk.Button(frame, text=location, width=30,
                      command=lambda loc=location: self.show_emails(loc)).pack(side="left")

            if self.is_admin:
                tk.Button(frame, text="✏️", fg="blue",
                          command=lambda loc=location: self.edit_location(loc)).pack(side="left", padx=5)

                tk.Button(frame, text="🗑️", fg="red",
                          command=lambda loc=location: self.delete_location(loc)).pack(side="left")

        if self.is_admin:
            tk.Button(self.root, text="➕ Dodaj lokalizację",
                      command=self.add_location, fg="green").pack(pady=15)

    def show_emails(self, location):
        emails = self.data[location]
        win = tk.Toplevel(self.root)
        win.title(f"E-maile - {location}")
        win.geometry("500x300")

        email_text = tk.Text(win, height=10, font=("Courier New", 11))
        email_text.insert("1.0", "\n".join(emails))
        email_text.configure(state="disabled")
        email_text.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)

        def copy_emails():
            self.root.clipboard_clear()
            self.root.clipboard_append("\n".join(emails))
            messagebox.showinfo("Skopiowano", "Adresy e-mail zostały skopiowane.")

        def send_outlook():
            email_string = ";".join(emails)
            subprocess.run(["outlook", "/c", "ipm.note", "/m", email_string], shell=True)

        tk.Button(button_frame, text="📧 Utwórz mail w Outlook", command=send_outlook).pack(side="left", padx=20)
        tk.Button(button_frame, text="📋 Kopiuj", command=copy_emails).pack(side="right", padx=20)

    def add_location(self):
        loc = simpledialog.askstring("Nowa lokalizacja", "Podaj nazwę:")
        if loc and loc not in self.data:
            emails_str = simpledialog.askstring("Adresy e-mail", "Oddzielone przecinkami:")
            if emails_str:
                self.data[loc] = [e.strip() for e in emails_str.split(",")]
                self.draw_interface()

    def edit_location(self, loc):
        emails_str = simpledialog.askstring("Edytuj", "Nowa lista e-mail (przecinkami):")
        if emails_str:
            self.data[loc] = [e.strip() for e in emails_str.split(",")]
            self.draw_interface()

    def delete_location(self, loc):
        if messagebox.askyesno("Potwierdź", f"Usunąć {loc}?"):
            del self.data[loc]
            self.draw_interface()

def login_screen():
    login = tk.Tk()
    login.title("Logowanie")
    login.geometry("350x160")

    def login_user():
        password = password_entry.get()
        login.destroy()
        root = tk.Tk()
        App(root, is_admin=(password == "Zaq12wsx"))
        root.mainloop()

    tk.Label(login, text="Hasło administratora (lub puste):").pack(pady=10)
    password_entry = tk.Entry(login, show="*")
    password_entry.pack(pady=5)
    tk.Button(login, text="Zaloguj", command=login_user).pack(pady=10)
    login.mainloop()

if __name__ == "__main__":
    login_screen()