# Load tasks from file
try:
    with open("tasks.txt", "r", encoding="utf-8") as file:
        tasks = file.read().splitlines()
except:
    tasks = []


def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")


while True:
    print("\n=== TASK MANAGER ===")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Edit task")
    print("5. Complete task")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == "1":
        task = input("Task: ")
        priority = input("Priority (HIGH/MEDIUM/LOW): ").upper()
        deadline = input("Deadline (YYYY-MM-DD): ")

        full_task = f"[{priority}] {task} | Due: {deadline}"
        tasks.append(full_task)

        save_tasks()
        print("Task added!")

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks")
        else:
            print("\nTasks:")
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")

    elif choice == "3":
        num = int(input("Delete number: "))

        if 0 < num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks()
            print(f"{removed} deleted")
        else:
            print("Invalid task number")

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

    elif choice == "5":
        num = int(input("Task number completed: "))

        if 0 < num <= len(tasks):
            if "[DONE]" not in tasks[num - 1]:
                tasks[num - 1] += " [DONE]"
            save_tasks()
            print("Task completed!")
        else:
            print("Invalid task number")

    elif choice == "6":
        print("Bye!")
        break

    else:
        print("Invalid choice")