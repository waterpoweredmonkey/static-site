from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        tag = self.tag
        if tag == None:
            raise ValueError("All ParentNodes must have a tag")
        if not self.children:
            raise ValueError("All ParentNodes must have children")
        
        return f"<{tag}>{"".join(child.to_html() for child in self.children)}</{tag}>"
