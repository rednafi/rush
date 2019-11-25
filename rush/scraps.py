a = {
    "task_1": ['echo "task1 is running"', "ls"],
    "task_2": ['echo "task2 is running"'],
    "task_3": ["task1", "task2"],
    "task_4": ["task3"],
}


def find(dictionary):
    for k, v in dictionary.items():
        if isinstance(v, list):
            for i in v:
                if isinstance(i, str) and i == k:
                    dictionary[k] = v

                yield dictionary


print(list(find(a)))
