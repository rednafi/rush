import yaml

with open("./Rushfile") as file:
    yml_content = yaml.load(file, Loader=yaml.FullLoader)
    # make sure the task names are strings
    yml_content = {str(k): v for k, v in yml_content.items()}
    print(yml_content)
