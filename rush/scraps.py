a = {
    "job1": ['echo "job1 is running"'],
    "job2": ['echo "job2 is running"'],
    "job3": ["job1", "job2"],
    "job4": ["job3"],
}


def find(dictionary):
    for k, v in dictionary.items():
        if isinstance(v, list):
            for i in v:
                if isinstance(i, str) and i == k:
                    dictionary[k] = v

                yield dictionary


print(list(find(a)))
