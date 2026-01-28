import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import os

# File to store courses and books
COURSE_FILE = "courses_data.txt"

# Default Knowledge Base
courses = {
    "Computer Science": "Programming",
    "Mechanical Engineering": "Thermodynamics",
    "Electrical Engineering": "Circuit Analysis",
    "Artificial Intelligence": "AI",
    "Machine Learning": "ML",
    "Cybersecurity": "Security",
    "Data Science": "Data Analysis",
    "Robotics": "Automation",
    "Physics": "Quantum Mechanics",
    "Bioinformatics": "Biology Data",

}

book_categories = {
    "Programming": ["Introduction to Python", "Data Structures in C"],
    "Thermodynamics": ["Fundamentals of Thermodynamics", "Heat Transfer"],
    "Circuit Analysis": ["Basic Electrical Circuits", "Power Systems Engineering"],
    "AI": ["Mathematics for Machine Learning", "Deep Learning with Python", "Neural Networks and Deep Learning"],
    "ML": ["Python Machine Learning", "Introduction to ML Algorithms", "Hands-On Machine Learning with Scikit-Learn"],
    "Security": ["Cybersecurity Essentials", "Network Security Principles", "Ethical Hacking"],
    "Data Analysis": ["Python for Data Analysis", "Big Data Analytics", "Data Visualization with Python"],
    "Automation": ["Introduction to Robotics", "Control Systems Engineering", "Autonomous Robots and AI"],
    "Quantum Mechanics": ["Quantum Mechanics Simplified", "Advanced Classical Mechanics", "Introduction to Astrophysics"],
    "Biology Data": ["Fundamentals of Bioinformatics", "Genomic Data Science", "Computational Biology"],
}


# Load Existing Courses (Handled Safely)
def load_courses():
    if os.path.exists(COURSE_FILE):
        try:
            with open(COURSE_FILE, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "|" in line:  # Ensure correct format
                        course, books = line.strip().split("|")
                        book_categories[course] = books.split(",")  # Store books properly
        except Exception as e:
            print(f"Error loading courses: {e}")

load_courses()  # Called after initialization

# User Credentials (Admin)
USER_CREDENTIALS = {"admins": "123456"}

# Inference Engine
def recommend_books(course):
    return book_categories.get(course, [])

# Multi-Page Application Class
class MultiPageApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Book Recommendation System")
        self.root.geometry("500x400")

        # Text-to-Speech Engine
        self.tts_engine = pyttsx3.init()

        self.pages = {}

        self.create_start_page()
        self.create_user_selection_page()
        self.create_learner_page()
        self.create_login_page()
        self.create_admin_page()

        self.show_page("Start")

    def show_page(self, page_name):
        """Displays the requested page."""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)

    def create_start_page(self):
        page = tk.Frame(self.root)
        ttk.Label(page, text="Welcome!", font=("Arial", 16)).pack(pady=20)
        ttk.Button(page, text="Start", command=lambda: self.show_page("UserSelection")).pack(pady=10)
        self.pages["Start"] = page

    def create_user_selection_page(self):
        page = tk.Frame(self.root)
        ttk.Label(page, text="Select User Type", font=("Arial", 14)).pack(pady=20)
        ttk.Button(page, text="Learner", command=lambda: self.show_page("Learner")).pack(pady=10)
        ttk.Button(page, text="User", command=lambda: self.show_page("Login")).pack(pady=10)
        self.pages["UserSelection"] = page

    def create_learner_page(self):
        page = tk.Frame(self.root)
        ttk.Label(page, text="Select Your Course:", font=("Arial", 12)).pack(pady=10)
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(page, textvariable=self.course_var, values=list(book_categories.keys()))
        self.course_dropdown.pack(pady=10)

        ttk.Button(page, text="Recommend Books", command=self.display_recommendations).pack(pady=15)
        self.result_label = ttk.Label(page, text="", wraplength=400)
        self.result_label.pack(pady=15)

        ttk.Button(page, text="Back", command=lambda: self.show_page("UserSelection")).pack(pady=10)
        self.pages["Learner"] = page

    def display_recommendations(self):
        course = self.course_var.get()
        books = recommend_books(course)
        if books:
            recommendations = f"Recommended Books for {course}:\n" + "\n".join(books)
            self.result_label.config(text=recommendations)
        else:
            self.result_label.config(text="No books found for this course.")

    def create_login_page(self):
        page = tk.Frame(self.root)
        ttk.Label(page, text="User Login", font=("Arial", 14)).pack(pady=20)
        ttk.Label(page, text="User ID:").pack()
        self.user_id_entry = ttk.Entry(page)
        self.user_id_entry.pack(pady=5)

        ttk.Label(page, text="Password:").pack()
        self.password_entry = ttk.Entry(page, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(page, text="Login", command=self.validate_login).pack(pady=15)
        ttk.Button(page, text="Back", command=self.clear_credentials_and_go_back).pack(pady=10)

        self.pages["Login"] = page

    def validate_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if USER_CREDENTIALS.get(user_id) == password:
            messagebox.showinfo("Login Successful", "Welcome admin!")
            self.show_page("Admin")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials! Try again.")

    def clear_credentials_and_go_back(self):
        """Clear credentials when user goes back."""
        self.user_id_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.show_page("UserSelection")
    def create_admin_page(self):
        page = tk.Frame(self.root)
        ttk.Label(page, text="Admin Page", font=("Arial", 14)).pack(pady=20)

        # Adding Courses
        ttk.Label(page, text="Add New Course:").pack()
        self.new_course_entry = ttk.Entry(page)
        self.new_course_entry.pack(pady=5)

        ttk.Label(page, text="Add Recommended Books (Comma-separated):").pack()
        self.new_books_entry = ttk.Entry(page)
        self.new_books_entry.pack(pady=5)

        ttk.Button(page, text="Add Course", command=self.add_new_course).pack(pady=10)

        # Deleting Courses
        ttk.Label(page, text="Delete Course:").pack()
        self.delete_course_entry = ttk.Entry(page)
        self.delete_course_entry.pack(pady=5)

        ttk.Button(page, text="Delete Course", command=self.delete_course).pack(pady=10)

        ttk.Button(page, text="Logout", command=self.clear_credentials_and_go_back).pack(pady=10)

        self.pages["Admin"] = page
    def add_new_course(self):
        course_name = self.new_course_entry.get().strip()
        books = self.new_books_entry.get().strip().split(",")

        if course_name and books:
            book_categories[course_name] = books

            with open(COURSE_FILE, "a") as file:
                file.write(f"{course_name}|{','.join(books)}\n")

            messagebox.showinfo("Success", f"Course '{course_name}' added successfully!")
            self.new_course_entry.delete(0, tk.END)
            self.new_books_entry.delete(0, tk.END)
            self.course_dropdown["values"] = list(book_categories.keys())  # Update dropdown
        else:
            messagebox.showerror("Error", "Please enter a valid course name and books.")
    def delete_course(self):
        course_name = self.delete_course_entry.get().strip()

        if course_name in book_categories:
            del book_categories[course_name]

            with open(COURSE_FILE, "w") as file:
                for course, books in book_categories.items():
                    file.write(f"{course}|{','.join(books)}\n")

            messagebox.showinfo("Success", f"Course '{course_name}' deleted successfully!")
            self.delete_course_entry.delete(0, tk.END)
            self.course_dropdown["values"] = list(book_categories.keys())
        else:
            messagebox.showinfo("delete page", "the course is not found")
if _name_ == "_main_":
    root = tk.Tk()
    app = MultiPageApp(root)
    root.mainloop()
