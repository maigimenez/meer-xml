from collections import defaultdict, deque

class Tree():
    """Tree Object, contains value and child references"""
    def __init__(self, value=None, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children

    def breadthFirst(self):
        """Sequentially yield nodes in an unguided breadthFirst fashion"""
        q = deque([self])
        while len(q) > 0:
            node = q.popleft()
            yield node.value
            for child in node.children:
                q.append(child)
        return

    # def orderedTraversal(self, mode):
    #     '''Defaults to preorder'''
    #     q = deque([self])
    #     while len(q) > 0:
    #         node = q.popleft()
    #         yield node
    #         aux = deque()
    #         for i in node.children:
    #             aux.append(node.children[i])
    #         if mode == "preorder":
    #             q.extend(aux)
    #         elif mode == "postorder":
    #             aux.reverse()
    #             q.extend(aux)
    #         else:
    #             q.extend(aux)
    #     return

    def depthFirst(self):
        """Sequentially yield nodes in an unguided depth-first fashion"""
        q = deque([self])
        while len(q) > 0:
            node = q.pop()
            yield node.value
            for child in node.children:
                q.append(child)
        return

    def depthFirstChildren(self):
        """Sequentially yield nodes and its children in an unguided depth-first fashion"""
        q = deque([self])
        while len(q) > 0:
            node = q.pop()
            yield node.value, node.children
            for child in node.children:
                q.append(child)
        return

    def __contains__(self, item):
        """Uses Breadth-first search to find Trees"""
        if item is self:
            return True
        else:
            for node in self.breadthFirst():
                if node is item:
                    return True
            return False

    def clear(self):
        """ Clear tree structure """
        self.value = None
        self.children.clear()
    
    def get_set_data(self,containers,attributes):
        """ Return a set of containers and a set of its attributes"""
        written_codes = []
        for container in self.breadthFirst():
            schema_code = container.get_schema_code()
            if schema_code not in written_codes:
                containers.append(container)
                written_codes.append(schema_code)
            for attribute in container.attributes:
                schema_code = attribute.get_schema_code()
                if schema_code not in written_codes:
                    attributes.append(attribute)
                    written_codes.append(schema_code)
        return (containers,attributes) 

    def is_leaf(self):
        """ Return true if this tree hasn't got children"""
        return self.children == []

    def print_tree(self,ident):
        """ Dicom tree  Pretty print """
        if (self.value):
            # TODO: Check a better way to do this
            # Get node meaning in first defined language. 
            meaning = self.value.concept.meaning.values()[0]
            # Get the attributes formated to print them. 
            str_attributes = '\n'
            for attribute in self.value.attributes:
                str_attributes += ("|" + " " * (ident + 2) + " - "
                                   + attribute.__str__() + '\n')
            str_attributes = str_attributes[:-1]
            # Print this level 
            print u"{0} [{1}_{2}] {3} (no.attr: {4} ) (prop: {5}) {6}"\
                .format("-" * (ident + 1), self.value.concept.schema, 
                        self.value.concept.value, meaning.upper(),
                        len(self.value.attributes), self.value.properties, 
                        str_attributes)
            # Print its children
            for child in self.children:
                child.print_tree(ident+4)


    def add_node(self, container, parent):
        """ Adds a container node to the tree. 

        Keyword Arguments:
        container -- node to add. 
        parent -- parent concept of node to add
        """
        if parent == None:
            self.__init__(container, None)
        else:
            if(self.value.has_code(parent.get_schema_code())):
                self.children.append(Tree(container))
            else:
                for child in self.children:
                    child.add_node(container,parent)


    def get_flat_tree(self,flat):
        """ Return a hash table with the tree. 
        It loses tree level information """
        if (self.is_leaf()):
            flat[self.value] = []
            return (flat)
        else:
            children = [child.value for child in self.children]
            flat[self.value] = children
            for child in self.children:
                    child.get_flat_tree(flat)


    def get_code_containers(self):
        """ Return a set of schema_code values for every CODE attribute.""" 
        codes = []
        written_codes = []
        for container in self.breadthFirst():
            for attribute in container.attributes:
                if (attribute.type == 'code'):
                    schema_code = attribute.get_schema_code()
                    if schema_code not in written_codes:
                        codes.append(attribute)
                        written_codes.append(schema_code)
        return codes

