from src.htmlnode import HTMLNode


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
