from os import mkdir, path


def create_dir_if_absent(directory):
    if path.isdir(directory) is False:
        try:
            mkdir(directory)
        except OSError:
            print("UNISCAN: Creating %s FAILED ! Exiting :(" % directory)
            return -1
        else:
            print(
                "UNISCAN: The directory %s didnt exist, so its been created."
                % directory
            )
