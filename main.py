# ===============================
# TASKMANAGER PRO
# Simple task manager using Python
# Features:
# Add / Show / Delete / Edit / Complete / Search / Sort / Save
# ===============================


# ===== Load tasks from tasks.txt =====
# This part tries to read old tasks from the file.
# If the file does not exist, it starts with an empty list.
try:
    with open("tasks.txt", "r", encoding="utf-8") as file:
        tasks = file.read().splitlines()
except:
    tasks = []


# ===== Save tasks function =====
# This function saves all tasks inside tasks.txt.
# We use it after add, delete, edit, complete, and sort.
def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")


# ===== Main menu loop =====
# while True means the program keeps running until the user chooses Exit.
while True:
    print("\n=== TASK MANAGER ===")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Edit task")
    print("5. Complete task")
    print("6. Search task")
    print("7. Sort tasks by priority")
    print("8. Exit")

    choice = input("Choose: ")


    # ===== 1. Add task =====
    # User enters task name, priority, and deadline.
    if choice == "1":
        task = input("Task: ")
        priority = input("Priority (HIGH/MEDIUM/LOW): ").upper()
        deadline = input("Deadline (YYYY-MM-DD): ")

        full_task = f"[{priority}] {task} | Due: {deadline}"
        tasks.append(full_task)

        save_tasks()
        print("Task added!")


    # ===== 2. Show tasks =====
    # Displays all saved tasks with numbers.
    elif choice == "2":
        print("\nTasks:")

        if not tasks:
            print("No tasks")
        else:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")


    # ===== 3. Delete task =====
    # User chooses the task number to delete.
    elif choice == "3":
        num = int(input("Delete number: "))

        if 0 < num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks()
            print(f"{removed} deleted")
        else:
            print("Invalid task number")


    # ===== 4. Edit task =====
    # User chooses a task number and replaces it with new information.
    elif choice == "4":
        num = int(input("Edit number: "))

        if 0 < num <= len(tasks):
            task = input("New task: ")
            priority = input("Priority (HIGH/MEDIUM/LOW): ").upper()
            deadline = input("Deadline (YYYY-MM-DD): ")

            tasks[num - 1] = f"[{priority}] {task} | Due: {deadline}"
            save_tasks()
            print("Task updated!")
        else:
            print("Invalid task number")


    # ===== 5. Complete task =====
    # Adds [DONE] to a task when it is completed.
    elif choice == "5":
        num = int(input("Task number completed: "))

        if 0 < num <= len(tasks):
            if "[DONE]" not in tasks[num - 1]:
                tasks[num - 1] += " [DONE]"

            save_tasks()
            print("Task completed!")
        else:
            print("Invalid task number")


    # ===== 6. Search task =====
    # Searches for tasks using a keyword.
    elif choice == "6":
        keyword = input("Search keyword: ").lower()
        print("\nSearch results:")

        found = False

        for i, task in enumerate(tasks):
            if keyword in task.lower():
                print(f"{i+1}. {task}")
                found = True

        if not found:
            print("No matching tasks found.")


    # ===== 7. Sort tasks by priority =====
    # Sorts tasks: HIGH first, then MEDIUM, then LOW.
    elif choice == "7":
        priority_order = {
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        tasks.sort(
            key=lambda task:
            priority_order.get(
                task.split("]")[0].replace("[", ""),
                99
            )
        )

        save_tasks()
        print("Tasks sorted by priority!")


    # ===== 8. Exit =====
    # Stops the program.
    elif choice == "8":
        print("Bye!")
        break


    # ===== Invalid choice =====
    # Runs when user enters a wrong option.
    else:
        print("Invalid choice")