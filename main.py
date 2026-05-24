tasks = []

while True:
    print("\n=== TASK MANAGER ===")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        task = input("Enter task: ")
        tasks.append(task)
        print("Task added!")

    elif choice == "2":
        print("\nTasks:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")

    elif choice == "3":
        num = int(input("Task number to delete: "))
        if 0 < num <= len(tasks):
            removed = tasks.pop(num-1)
            print(f"{removed} deleted")

    elif choice == "4":
        print("Bye!")
        break

    else:
        print("Invalid choice")