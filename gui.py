import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json

tasks = []
current_indices = []
notified_tasks = set()

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except:
        tasks = []

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def get_due_datetime(task):
    try:
        due = task.split("Due:")[1].strip().split(" [")[0]
        return datetime.strptime(due, "%Y-%m-%d %I:%M %p")
    except:
        return None

def refresh(task_list=None):
    global current_indices

    listbox.delete(0, tk.END)
    current_indices = []

    display_tasks = task_list if task_list is not None else list(enumerate(tasks))

    done = 0
    overdue = 0
    now = datetime.now()

    for real_index, task in display_tasks:
        color = "white"
        text = task

        if "[DONE]" in task:
            done += 1

        due_date = get_due_datetime(task)

        if due_date and "[DONE]" not in task:
            days_left = (due_date - now).days

            if due_date < now:
                color = "red"
                overdue += 1
                text += " [OVERDUE]"
            else:
                text += f" ({days_left}d left)"

        listbox.insert(tk.END, text)
        listbox.itemconfig(tk.END, fg=color)
        current_indices.append(real_index)

    total = len(tasks)
    progress["value"] = (done / max(total, 1)) * 100
    stats_label.config(text=f"Tasks: {total}   |   Done: {done}   |   Overdue: {overdue}")

def add_task():
    task = task_entry.get().strip()
    priority = priority_box.get()
    date = date_entry.get()
    hour = hour_box.get()
    minute = minute_box.get()
    ampm = ampm_box.get()

    if task == "":
        messagebox.showwarning("Warning", "Task is empty")
        return

    new_task = f"[{priority}] {task} | Due:{date} {hour}:{minute} {ampm}"
    tasks.append(new_task)

    save_tasks()
    refresh()
    task_entry.delete(0, tk.END)

def delete_task():
    selected = listbox.curselection()

    if selected:
        real_index = current_indices[selected[0]]
        tasks.pop(real_index)
        save_tasks()
        refresh()
    else:
        messagebox.showwarning("Warning", "Select a task first")

def complete_task():
    selected = listbox.curselection()

    if selected:
        real_index = current_indices[selected[0]]

        if "[DONE]" not in tasks[real_index]:
            tasks[real_index] += " [DONE]"

        save_tasks()
        refresh()
    else:
        messagebox.showwarning("Warning", "Select a task first")

def sort_tasks():
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

    tasks.sort(
        key=lambda task: order.get(task.split("]")[0].replace("[", ""), 99)
    )

    save_tasks()
    refresh()

def search_tasks():
    keyword = search_entry.get().lower().strip()

    if keyword == "":
        refresh()
        return

    results = []

    for i, task in enumerate(tasks):
        if keyword in task.lower():
            results.append((i, task))

    refresh(results)

def export_tasks():
    with open("my_tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")

    messagebox.showinfo("Export", "Tasks exported to my_tasks.txt")

def update_clock():
    clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, update_clock)

def check_reminders():
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    for task in tasks:
        if "[DONE]" in task:
            continue

        due_date = get_due_datetime(task)

        if due_date:
            due_text = due_date.strftime("%Y-%m-%d %I:%M %p")

            if due_text == now and task not in notified_tasks:
                notified_tasks.add(task)
                messagebox.showwarning("Reminder", f"Deadline reached:\n{task}")

    root.after(30000, check_reminders)

# Window
root = tk.Tk()
root.title("TaskManager Pro")
root.geometry("900x720")
root.configure(bg="#121212")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "green.Horizontal.TProgressbar",
    background="#00ff55",
    troughcolor="#333333",
    thickness=20
)

main = tk.Frame(root, bg="#121212")
main.pack(fill="both", expand=True)

clock_label = tk.Label(main, bg="#121212", fg="white", font=("Arial", 14))
clock_label.pack(pady=3)

title_label = tk.Label(
    main,
    text="TaskManager Pro",
    bg="#121212",
    fg="white",
    font=("Arial", 32, "bold")
)
title_label.pack(pady=10)

form = tk.Frame(main, bg="#121212")
form.pack()

tk.Label(form, text="Task", bg="#121212", fg="white").grid(row=0, column=0, columnspan=3)
task_entry = tk.Entry(form, width=55, font=("Arial", 12))
task_entry.grid(row=1, column=0, columnspan=3, pady=5)

tk.Label(form, text="Priority", bg="#121212", fg="white").grid(row=2, column=0)
priority_box = ttk.Combobox(form, values=["HIGH", "MEDIUM", "LOW"], width=15, state="readonly")
priority_box.grid(row=3, column=0, padx=5, pady=5)
priority_box.set("HIGH")

tk.Label(form, text="Date", bg="#121212", fg="white").grid(row=2, column=1)
date_entry = DateEntry(form, date_pattern="yyyy-mm-dd", width=15)
date_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(form, text="Time", bg="#121212", fg="white").grid(row=2, column=2)
time_frame = tk.Frame(form, bg="#121212")
time_frame.grid(row=3, column=2, padx=5, pady=5)

hour_box = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(1, 13)], width=4, state="readonly")
hour_box.grid(row=0, column=0)
hour_box.set("12")

minute_box = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=4, state="readonly")
minute_box.grid(row=0, column=1)
minute_box.set("00")

ampm_box = ttk.Combobox(time_frame, values=["AM", "PM"], width=4, state="readonly")
ampm_box.grid(row=0, column=2)
ampm_box.set("PM")

buttons_frame = tk.Frame(main, bg="#121212")
buttons_frame.pack(pady=8)

buttons = [
    ("Add", "#00aa00", add_task),
    ("Delete", "#ff2222", delete_task),
    ("Complete", "#0066ff", complete_task),
    ("Sort", "#9900cc", sort_tasks),
    ("Export TXT", "#444444", export_tasks),
]

for i, (text, color, command) in enumerate(buttons):
    tk.Button(
        buttons_frame,
        text=text,
        bg=color,
        fg="white",
        width=14,
        height=2,
        bd=0,
        command=command
    ).grid(row=0, column=i, padx=5)

progress = ttk.Progressbar(main, length=650, style="green.Horizontal.TProgressbar")
progress.pack(pady=10)

stats_label = tk.Label(main, bg="#121212", fg="white", font=("Arial", 15, "bold"))
stats_label.pack(pady=5)

search_frame = tk.Frame(main, bg="#121212")
search_frame.pack(pady=6)

search_entry = tk.Entry(search_frame, width=45, font=("Arial", 12))
search_entry.grid(row=0, column=0, padx=5)

tk.Button(
    search_frame,
    text="Search",
    bg="orange",
    fg="white",
    width=15,
    bd=0,
    command=search_tasks
).grid(row=0, column=1, padx=5)

list_frame = tk.Frame(main, bg="#121212")
list_frame.pack(pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(
    list_frame,
    width=100,
    height=12,
    font=("Arial", 12),
    bg="#222222",
    fg="white",
    yscrollcommand=scrollbar.set
)
listbox.pack(side="left", fill="both", expand=True)

scrollbar.config(command=listbox.yview)

load_tasks()
refresh()
update_clock()
check_reminders()

root.mainloop()