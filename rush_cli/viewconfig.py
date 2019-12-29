from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    String,
)


class YourStyle(Style):
    default_style = ""
    styles = {
        Comment: "italic #888",
        Keyword: "bold #005",
        Name: "#f00",
        Name.Function: "#0f0",
        Name.Class: "bold #0f0",
        String: "bg:#eee #111",
    }
