import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx", ".xls"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"],
    "Programs": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css",".exe"],
    "Archives": [".zip", ".rar", ".7z"]
}

# Organize files
def organize_files():
    path = folder_path.get()

    if not path:
        messagebox.showerror("Error", "Please select a folder first")
        return

    files = os.listdir(path)

    total_files = 0
    for file in files:
        if os.path.isfile(os.path.join(path, file)) and file != "organizer_log.txt":
            total_files += 1

    status_label.config(text=f"Status: Found {total_files} files. Organizing...")
    root.update_idletasks()

    log_file = os.path.join(path, "organizer_log.txt")
    moved_files = 0

    try:
        with open(log_file, "w") as log:

            for file in files:

                file_path = os.path.join(path, file)

                if os.path.isfile(file_path) and file != "organizer_log.txt":

                    filename, extension = os.path.splitext(file)
                    moved = False

                    for folder, extensions in file_types.items():

                        if extension.lower() in extensions:

                            folder_dir = os.path.join(path, folder)

                            if not os.path.exists(folder_dir):
                                os.makedirs(folder_dir)

                            shutil.move(file_path, os.path.join(folder_dir, file))
                            log.write(f"{file}|{folder}\n")

                            moved_files += 1
                            moved = True
                            break

                    if not moved:

                        other_folder = os.path.join(path, "Others")

                        if not os.path.exists(other_folder):
                            os.makedirs(other_folder)

                        shutil.move(file_path, os.path.join(other_folder, file))
                        log.write(f"{file}|Others\n")

                        moved_files += 1

        messagebox.showinfo("Success", f"{moved_files} files organized successfully!")
        status_label.config(text=f"Status: {moved_files} files organized successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Status: Error occurred")


# Restore files
def restore_files():

    path = folder_path.get()

    if not path:
        messagebox.showerror("Error", "Please select a folder first")
        return

    log_file = os.path.join(path, "organizer_log.txt")

    if not os.path.exists(log_file):
        messagebox.showerror("Error", "No restore data found!")
        return

    status_label.config(text="Status: Restoring files...")
    root.update_idletasks()

    try:

        with open(log_file, "r") as log:
            lines = log.readlines()

        restored = 0

        for line in lines:

            file, folder = line.strip().split("|")

            source = os.path.join(path, folder, file)
            destination = os.path.join(path, file)

            if os.path.exists(source):
                shutil.move(source, destination)
                restored += 1

        # Remove empty folders
        for folder in list(file_types.keys()) + ["Others"]:

            folder_path_check = os.path.join(path, folder)

            if os.path.exists(folder_path_check):

                try:
                    if len(os.listdir(folder_path_check)) == 0:
                        os.rmdir(folder_path_check)
                except:
                    pass

        os.remove(log_file)

        messagebox.showinfo("Success", f"{restored} files restored successfully!")
        status_label.config(text=f"Status: {restored} files restored successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Status: Error occurred")


# Browse folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


# GUI Window
root = tk.Tk()
root.title("Automatic File Organizer")
root.geometry("450x270")
root.resizable(False, False)

folder_path = tk.StringVar()

# Title
title = tk.Label(root, text="Automatic File Organizer", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Folder label
label = tk.Label(root, text="Select Folder:")
label.pack()

# Entry box
entry = tk.Entry(root, textvariable=folder_path, width=45)
entry.pack(pady=5)

# Browse button
browse_btn = tk.Button(root, text="Browse Folder", command=browse_folder, width=20)
browse_btn.pack(pady=5)

# Organize button
organize_btn = tk.Button(root, text="Organize Files", command=organize_files, width=20, bg="lightgreen")
organize_btn.pack(pady=10)

# Restore button
restore_btn = tk.Button(root, text="Restore Files", command=restore_files, width=20, bg="lightblue")
restore_btn.pack(pady=5)

# Status bar
status_label = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor="w")
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Run program
root.mainloop()
