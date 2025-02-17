from htmlnode import HTMLNode

class LeafNode(HTMLNode): 
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, props = props)

    def to_html(self):
        tag = self.tag
        if self.value == None:
            raise ValueError("All LeafNodes must have a value")
        if tag == None:
            return self.value
        
        return f"<{tag}{self.props_to_html()}>{self.value}</{tag}>"