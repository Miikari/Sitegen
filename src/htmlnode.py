class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        result = []
        for key, value in self.props.items():
            result.append(f' {key}="{value}"')
        return "".join(result)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

        


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None or not isinstance(self.value, str):
            raise ValueError
        if not self.tag:
            return self.value
        prop = ""
        if self.props:
            for key, value in self.props.items():
                prop += ' '+key + "=" + '"'+value+'"'

        return f"<{self.tag}{prop}>{self.value}</{self.tag}>" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag found")
        if not self.children:
            raise ValueError("No children found")
        childs = []
        for c in self.children:
            childs.append(c.to_html())
        lst = "".join(childs)
        prop = ""
        if self.props:
            for key, value in self.props.items():
                prop = ' '+key + "=" + '"'+value+'"'

        return f"<{self.tag}{prop}>{lst}</{self.tag}>"