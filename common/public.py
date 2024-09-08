import datetime


def print_format(msg, color=None):
    if color == "red":
        color_s = "\033[31m"
    elif color == "green":
        color_s = "\033[32m"
    elif color == "yellow":
        color_s = "\033[33m"
    elif color == "blue":
        color_s = "\033[34m"
    else:
        color_s = ""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = current_date + " : " + "{}".format(msg)
    if color_s == "":
        print(msg)
    else:
        print(color_s + msg + "\033[0m")


if __name__ == "__main__":
    print_format("hello world", "red")
    print_format("hello world")
