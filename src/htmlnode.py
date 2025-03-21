

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f" {key}=\"{value}\"" for key, value in self.props.items())
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode): 
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        tag = self.tag
        if self.value is None:
            raise ValueError("All LeafNodes must have a value")
        if tag is None:
            return self.value
        
        return f"<{tag}{self.props_to_html()}>{self.value}</{tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        tag = self.tag
        if tag == None:
            raise ValueError("All ParentNodes must have a tag")
        if not self.children:
            raise ValueError("All ParentNodes must have children")
        
        return f"<{tag}>{"".join(child.to_html() for child in self.children)}</{tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"