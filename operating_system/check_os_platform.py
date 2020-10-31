import os

def get_os_platform1():
    from sys import platform
    print(platform)
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "OS X"
    elif platform == "win32":
        return "Windows"
    else:
        return None

def get_os_platform2():
    import platform
    system_platform = platform.system()
    print(system_platform)
    if system_platform == "linux" or system_platform == "linux2":
        return "linux"
    elif system_platform == "Darwin":
        return "OS X"
    elif system_platform == "win32":
        return "Windows"
    else:
        return None

if __name__ == "__main__":
    print(get_os_platform1())
    print(get_os_platform2())