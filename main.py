"""main.py"""

import json


def get_list():
    """opens the file called to-do.json, loads using json.load,
    and returns the loaded json object"""
    with open('to-do.json', encoding='utf-8') as file:
        to_do_list = json.load(file)
    return to_do_list


def save_list():
    """opens the to-do.json file, and writes td_list in json formatting with two spaces
     for indentation"""
    with open('to-do.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(td_list, indent=2))


def list_length():
    """returns the length of our list"""
    return len(td_list)


def add_task(task):
    """creates a dictionary object of a unchecked task, and appends the object to the to-do list"""
    task_json = {
        'name': task,
        'done': False
    }
    td_list.append(task_json)


def complete_task(task):
    """marks the task as complete, selected by it's number"""
    try:
        td_list[int(task) - 1]['done'] = True
    except ValueError:
        print('Sorry, you have to enter an integer')
        return
    except IndexError:
        print('Sorry, you have to enter a number in the list')
        return
    print('Done')


def remove_complete():
    """removes the complete tasks"""
    for i in range(len(td_list)-1,-1,-1):  # this range counts down instead of up
        if td_list[i]['done']:
            td_list.pop(i)


def generate_delete_check(task, multiple=False):
    """generates a delete check question"""
    if not multiple:
        output = 'Are you sure you want to delete the task "'
        output += task['name'] + '"? '
        output += '(done)' if task['done'] else '(Not done)'
        output += '\n(y/n): '
        return output
    output = 'Are you sure you want to delete the task "'
    output += td_list[task[0]]['name'] + '"'      # < when generate_delete_check is called with
    output += ' (' + str(len(task)) + ')? '       # | multiple set to True, the variable 'task' is a
    output += '\n(y/n)'                           # | list of indices, so we have to access the item
    return output                                 # | in 'td_list' instead of 'task'


def remove_task(input_task, protection: bool):
    """removes the task (can be number or name of task),
    if protection is true, asks the user before deleting task"""
    # if the user entered an int and if the number is in the range
    if isinstance(input_task, int) and (input_task in range(1, list_length())):
        # defines delete_check for 'are you sure you want to delete {name} {done\not done}'
        delete_check = generate_delete_check(td_list[input_task - 1])

        # if there is no protection, or the user says yes, remove the task, else do not delete
        if (not protection) or (input(delete_check).lower() == 'y'):
            td_list.pop(input_task - 1)
            return
        else:
            print("Ok, will not delete")
            return

    # if input_task is a string, searches for a task of the same name
    elif isinstance(input_task, str):
        found_tasks = []
        # finds all tasks that have the input name
        for i, task in enumerate(td_list):
            if task['name'] == input_task:
                found_tasks.append(i)            # note that the indices will be in ascending order

        if len(found_tasks) == 0:
            print('Sorry, we couldn\'t find any tasks by that name')
            return

        # if only one task was found, deletes, and asks if necessary
        if len(found_tasks) == 1:
            delete_check = generate_delete_check(td_list[found_tasks[0]])
            if (not protection) or (input(delete_check).lower == 'y'):
                td_list.pop(found_tasks[0])
                return
            print("Ok, will not delete")
            return

        # if we are here, it means that more than one task was found
        delete_check = generate_delete_check(found_tasks, True)
        if (not protection) or (input(delete_check).lower == 'y'):
            for i in found_tasks.reverse():              # < We have to reverse the list of indices
                td_list.pop(i)                           # | so that we don't delete the wrong items
            return

        print('Ok, will not delete')

    else:
        print('Sorry, we couldn\'t delete that task')


def display_list():
    """prints the to do list to the console"""
    # if the list is empty, tell the user so
    if list_length() == 0:
        print("Your list is empty. Try adding a task by saying \'add\'")
        return

    # otherwise, print out each item of the list along with a check if the item is marked as done
    print('Here is your list:')
    i = 1
    for task in td_list:
        print(i, ('\t[✓]' if task['done'] else '\t[ ]'), task['name'])
        i += 1
    print()


def display_help():
    """lists help page"""
    print('Here are your possible commands:')
    print(' list               - Lists your tasks')
    print(' add                - Adds a task to the list')
    print(' complete           - Marks a task as "done"')
    print(' remove complete    - Deletes all tasks marked as "done"')
    print(' delete             - Deletes a specific task from the list')
    print(' save               - Saves list to disk')
    print(' exit               - Exits this program, and saves list to disk')
    print(' help               - Displays this list')


def main_loop():
    """main functional loop"""
    # gets input from user
    input_text = input('> ').lower()
    # this loop will stop when the user enters 'exit'
    while not input_text == 'exit':
        # horribly long if statement which loops through all the commands
        if input_text == 'list':
            display_list()
        elif input_text == 'add':
            print('Enter the name of the task you want to add:')
            add_task(input('> '))
            print('Done')
        elif input_text == 'complete':
            print('Enter the number of the task you want to complete:')
            complete_task(input('> '))
        elif input_text == 'remove complete':
            remove_complete()
            print('Done')
        elif input_text == 'save':
            print('Saving...')
            save_list()
            print('Done')
        elif input_text == 'delete':
            print('Enter the name or number of the task you want to delete')
            remove_task(int(input('> ')), True)                   # TODO make this better
            print('Done')
        elif input_text == 'help':
            display_help()
        else:
            print('Sorry, but', input_text, 'is not a valid command')
            print('Say help for list of commands')
        input_text = input('> ').lower()


if __name__ == '__main__':
    td_list = get_list()
    print('Welcome to "to do list"')
    print('Say "help" for commands\n')
    display_list()
    main_loop()
    print('Thanks for using "to do list"')
    save_list()
