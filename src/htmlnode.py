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
        return "".join(f' {k}="{v}"' for k, v in self.props.items())
