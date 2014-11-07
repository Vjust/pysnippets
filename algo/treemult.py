global num_ops

class TreeNode:

    def __init__ (self, slice, parent, level):
        self.product = 1
        self.parent = parent
        self.children = []
        self.siblings = []
        self.slice = slice
        self.level = level
        for i in slice:
            self.product = mymult(self.product,i)

    def firstChild(self):
        return self.children[0]

    def secondChild(self):
        return self.children[1]

    def __repr__ (self):
        childCount = 0
        if self.children:
            childCount = len(self.children)
        return "<TreeNode: slice: {0}, level:{1} Children:{2} product {3}".\
                         format(self.slice, self.level, self.children, self.product)
        

def mymult (a,b):
    global num_ops
    num_ops += 1
    return a * b


def build_tree(l, parent = None, level=0 ):
    #print "build tree: slice {0} level {1}".format (l, level)
    if len(l) < 3:
        return []

    n = len(l)
    n2 = n / 2

    first_slice = l[0:n2]
    second_slice = l[n2: len(l)]

    new_level = level + 1
    first = TreeNode(first_slice, parent, new_level)
    second = TreeNode(second_slice, parent, new_level)

    first.siblings = second
    second.siblings = first

    first.children = build_tree (first_slice, first, new_level)
    second.children = build_tree (second_slice, second, new_level)

    return [first, second]


def compute_rest(a):

#    print "product in compute rest : {0}".format(product)

    # algorithm : for the 'first' leaf node, we will handle the leaf-node, and its sibling.
    # else : go up one level, compute sibling product.
    if a is None:
        return 1

#    sibling_product = 1
#    for i in a.siblings:
#        sibling_product *= i.product


    return mymult( a.siblings.product , compute_rest (a.parent))


def get_nodes(a):
    if a and a.children:
        for i in a.children:
            if i:
                print i
                get_nodes(i)


def get_leaf_nodes(a, l):
    if not a.children:
        l.append(a)
        return
    else:
        get_leaf_nodes (a.firstChild(),l)  # once for each sibling
        get_leaf_nodes (a.secondChild(),l)
    
def compute_all (a):
    global num_ops
    leaf = []
    result = []
    get_leaf_nodes (a, leaf)
    get_leaf_nodes (a.siblings, leaf)
    #print len(leaf)

    product = 1
    for i in leaf:
        
        #print i.slice
        product = compute_rest(i.parent)
        #print "product {0}".format(product) 
        if len(i.slice) == 2:
            result.append (product * i.slice[1] * i.siblings.product)
            result.append (product * i.slice[0] * i.siblings.product)
        elif len(i.slice) == 1:
            result.append (product * i.siblings.product)
            result.append (product * i.siblings.product)
    print num_ops
    num_ops=0
    return result
    
    
if __name__ == '__main__':
    num_ops = 0
    a,b = build_tree ([1,7,3,4,9, 8, 20])
    result = compute_all(a)
    print
