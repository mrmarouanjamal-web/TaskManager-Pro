# Load tasks from file
try:
    with open("tasks.txt", "r") as file:
        tasks = file.read().splitlines()
except:
    tasks = []

while True:
    print("\n=== TASK MANAGER ===")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Edit task")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        task = input("Enter task: ")
        tasks.append(task)

        with open("tasks.txt", "w") as file:
            for t in tasks:
                file.write(t + "\n")

        print("Task added!")

    elif choice == "2":
        print("\nTasks:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")

    elif choice == "3":
        num = int(input("Task number to delete: "))

        if 0 < num <= len(tasks):
            removed = tasks.pop(num - 1)

            with open("tasks.txt", "w") as file:
                for t in tasks:
                    file.write(t + "\n")

            print(f"{removed} deleted")
        else:
            print("Invalid task number")

    elif choice == "4":
        num = int(input("Task number to edit: "))

        if 0 < num <= len(tasks):
            old_task = tasks[num - 1]
            new_task = input("Enter new task: ")
            tasks[num - 1] = new_task

            with open("tasks.txt", "w") as file:
                for t in tasks:
                    file.write(t + "\n")

            print(f"{old_task} updated to {new_task}")
        else:
            print("Invalid task number")

    elif choice == "5":
        print("Bye!")
        break

    else:
        print("Invalid choice")