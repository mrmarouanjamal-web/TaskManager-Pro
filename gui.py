import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json

try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except:
    tasks = []

def save():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def update_clock():
    clock.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, update_clock)

def export_tasks():
    with open("my_tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")
    messagebox.showinfo("Done", "Tasks exported to my_tasks.txt")

def refresh():
    listbox.delete(0, tk.END)

    done = 0
    overdue = 0
    today = datetime.today()

    for task in tasks:
        color = "white"
        text = task

        try:
            due = task.split("Due:")[1].strip()

            try:
                due_date = datetime.strptime(due, "%Y-%m-%d %I:%M %p")
            except:
                due_date = datetime.strptime(due.split()[0], "%Y-%m-%d")

            days = (due_date - today).days

            if days < 0 and "[DONE]" not in task:
                color = "red"
                overdue += 1
                text += " ⚠ OVERDUE"
            elif "[DONE]" not in task:
                text += f" ({days}d left)"

        except:
            pass

        listbox.insert(tk.END, text)
        listbox.itemconfig(listbox.size() - 1, fg=color)

        if "[DONE]" in task:
            done += 1

    total = len(tasks)
    progress["value"] = (done / max(total, 1)) * 100
    stats.config(text=f"Tasks: {total}   |   Done: {done}   |   Overdue: {overdue}")

def add():
    task = task_entry.get()
    priority = priority_box.get()
    date = deadline.get()
    hour = hour_box.get()
    minute = minute_box.get()
    ampm = ampm_box.get()

    if task.strip() == "":
        messagebox.showwarning("Warning", "Task is empty")
        return

    full = f"[{priority}] {task} | Due:{date} {hour}:{minute} {ampm}"
    tasks.append(full)

    save()
    refresh()
    task_entry.delete(0, tk.END)

def delete():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        save()
        refresh()

def complete():
    selected = listbox.curselection()
    if selected:
        if "[DONE]" not in tasks[selected[0]]:
            tasks[selected[0]] += " ✅ [DONE]"
        save()
        refresh()

def search():
    key = search_entry.get().lower()
    listbox.delete(0, tk.END)

    for task in tasks:
        if key in task.lower():
            listbox.insert(tk.END, task)

def sort_tasks():
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    tasks.sort(key=lambda x: order.get(x.split("]")[0][1:], 99))
    save()
    refresh()

root = tk.Tk()
root.title("TaskManager Pro")
root.geometry("900x720")
root.configure(bg="#121212")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "green.Horizontal.TProgressbar",
    background="#00ff55",
    troughcolor="#333",
    thickness=20
)

main = tk.Frame(root, bg="#121212")
main.pack(fill="both", expand=True)

clock = tk.Label(main, font=("Arial", 14), bg="#121212", fg="white")
clock.pack(pady=3)
update_clock()

tk.Label(
    main,
    text="📝 TaskManager Pro",
    font=("Arial", 28, "bold"),
    bg="#121212",
    fg="white"
).pack(pady=10)

form = tk.Frame(main, bg="#121212")
form.pack()

tk.Label(form, text="Task", bg="#121212", fg="white").grid(row=0, column=0, pady=3)
task_entry = tk.Entry(form, width=50, font=("Arial", 12))
task_entry.grid(row=1, column=0, columnspan=3, pady=3)

tk.Label(form, text="Priority", bg="#121212", fg="white").grid(row=2, column=0, pady=3)
priority_box = ttk.Combobox(form, values=["HIGH", "MEDIUM", "LOW"], width=15, state="readonly")
priority_box.grid(row=3, column=0, pady=3)
priority_box.set("HIGH")

tk.Label(form, text="Date", bg="#121212", fg="white").grid(row=2, column=1, pady=3)
deadline = DateEntry(form, date_pattern="yyyy-mm-dd", width=15)
deadline.grid(row=3, column=1, pady=3)

tk.Label(form, text="Time", bg="#121212", fg="white").grid(row=2, column=2, pady=3)

time_frame = tk.Frame(form, bg="#121212")
time_frame.grid(row=3, column=2, pady=3)

hour_box = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(1, 13)], width=4, state="readonly")
hour_box.grid(row=0, column=0)
hour_box.set("12")

minute_box = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=4, state="readonly")
minute_box.grid(row=0, column=1)
minute_box.set("00")

ampm_box = ttk.Combobox(time_frame, values=["AM", "PM"], width=4, state="readonly")
ampm_box.grid(row=0, column=2)
ampm_box.set("PM")

btns = tk.Frame(main, bg="#121212")
btns.pack(pady=8)

buttons = [
    ("Add", "#00aa00", add),
    ("Delete", "#ff2222", delete),
    ("Complete", "#0066ff", complete),
    ("Sort", "#9900cc", sort_tasks),
    ("Export TXT", "#444444", export_tasks)
]

for i, (txt, color, cmd) in enumerate(buttons):
    tk.Button(
        btns,
        text=txt,
        bg=color,
        fg="white",
        width=14,
        height=2,
        bd=0,
        command=cmd
    ).grid(row=0, column=i, padx=5)

progress = ttk.Progressbar(main, length=650, style="green.Horizontal.TProgressbar")
progress.pack(pady=10)

stats = tk.Label(main, bg="#121212", fg="white", font=("Arial", 15, "bold"))
stats.pack(pady=5)

search_frame = tk.Frame(main, bg="#121212")
search_frame.pack(pady=6)

search_entry = tk.Entry(search_frame, width=45, font=("Arial", 12))
search_entry.grid(row=0, column=0, padx=5)

tk.Button(
    search_frame,
    text="Search 🔍",
    bg="orange",
    fg="white",
    width=15,
    bd=0,
    command=search
).grid(row=0, column=1, padx=5)

list_frame = tk.Frame(main, bg="#121212")
list_frame.pack(pady=10, fill="both", expand=True)

scroll = tk.Scrollbar(list_frame)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(
    list_frame,
    width=100,
    height=12,
    font=("Arial", 12),
    bg="#222222",
    fg="white",
    yscrollcommand=scroll.set
)
listbox.pack(side="left", fill="both", expand=True)

scroll.config(command=listbox.yview)

refresh()
root.mainloop()