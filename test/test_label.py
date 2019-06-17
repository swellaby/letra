from letra.label import Label

name = "bug"
description = "Something isn't working!"
color = "#d73a4a"
testLabel = Label(name=name, description=description, color=color)


def test_label_has_correct_name():
    assert testLabel.name == name


def test_label_has_correct_description():
    assert testLabel.description == description


def test_label_has_correct_color():
    assert testLabel.color == color
