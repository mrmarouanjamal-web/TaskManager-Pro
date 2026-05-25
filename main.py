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

    # Add task
    if choice == "1":
        task = input("Task: ")
        priority = input("Priority (HIGH/MEDIUM/LOW): ")

        full_task = f"[{priority}] {task}"
        tasks.append(full_task)

        save_tasks()
        print("Task added!")

    # Show tasks
    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks")
        else:
            print("\nTasks:")
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")

    # Delete task
    elif choice == "3":
        num = int(input("Delete number: "))

        if 0 < num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks()
            print(f"{removed} deleted")

    # Edit task
    elif choice == "4":
        num = int(input("Edit number: "))

        if 0 < num <= len(tasks):
            new_task = input("New task: ")
            tasks[num - 1] = new_task

            save_tasks()
            print("Task updated!")

    # Complete task
    elif choice == "5":
        num = int(input("Task number completed: "))

        if 0 < num <= len(tasks):
            tasks[num - 1] += " [DONE]"
            save_tasks()

            print("Task completed!")

    # Exit
    elif choice == "6":
        print("Bye!")
        break

    else:
        print("Invalid choice")