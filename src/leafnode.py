from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Invalid tag type: {type(tag).__name__}, expected a string or None"
            )

        if tag is not None and not isinstance(tag, str):
            raise ValueError(
                f"Invalid tag type: {type(tag).__name__}, expected a string or None"
            )

        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
