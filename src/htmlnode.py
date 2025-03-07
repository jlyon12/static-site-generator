import html


class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return (
            f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"
        )

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {k}="{html.escape(str(v))}"' for k, v in self.props.items())


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


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None or len(children) == 0:
            raise ValueError("ParentNode must have at least one child")
        if not isinstance(children, list):
            raise TypeError("children must be a list of HTMLNode instances")
        if not all(isinstance(child, HTMLNode) for child in children):
            raise TypeError("All children must be instances of HTMLNode")

        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        html = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html += child.to_html()

        return html + f"</{self.tag}>"
