from letra import Label
from io import StringIO, TextIOWrapper

bug_name = "bug"
bug_description = "Something isn't working!"
bug_color = "#d73a4a"
bug_label = Label(name=bug_name, description=bug_description, color=bug_color)

other_name = "other"
other_description = "Something different"
other_color = "#a24b2a"
other_label = Label(
    name=other_name, description=other_description, color=other_color
)

stub_labels = [bug_label, other_label]
stub_stream = TextIOWrapper(StringIO("", "\n"), "utf8", "", "\n", True, True)


def empty_mock(*unused):
    return ""
