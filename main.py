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
    print("4. Exit")

    choice = input("Choose: ")

    # Add task
    if choice == "1":
        task = input("Enter task: ")
        tasks.append(task)

        with open("tasks.txt", "w") as file:
            for t in tasks:
                file.write(t + "\n")

        print("Task added!")

    # Show tasks
    elif choice == "2":
        print("\nTasks:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")

    # Delete task
    elif choice == "3":
        num = int(input("Task number to delete: "))

        if 0 < num <= len(tasks):
            removed = tasks.pop(num - 1)

            with open("tasks.txt", "w") as file:
                for t in tasks:
                    file.write(t + "\n")

            print(f"{removed} deleted")

    # Exit
    elif choice == "4":
        print("Bye!")
        break

    else:
        print("Invalid choice")