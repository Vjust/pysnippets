"""
Dict Tree - prints out a nested dictionary in heirarchical form,
so that nested structures can be examined, especially where the dicts contain
lots of long text. Only structure is needed.

Usage : dict_tree (dict_name)

example input :

{'items': [{'snippet': 'abc'}],
 'jazz': 'music',
 'valarray': [{'base': {'j': 1, 'r': [10, 20, 30]}, 'id': 10}]}

example output (only dicts are printed) :

-->  ['items', 'jazz', 'valarray']
-->      items ['snippet']
-->      valarray ['base', 'id']
-->          base ['r', 'j']


"""


def dict_tree(in_dict, level=0, parent=""):
    """ recursive function to print dict heirarchy"""

    if not isinstance(in_dict, dict) and not isinstance(in_dict, list):
        return False

    try:
        if isinstance(in_dict, dict):
            tabs = "\t"*level
            print "-->{0} {1} {2}".format(tabs, str(parent), in_dict.keys())
            for i in in_dict.keys():
                dict_tree(in_dict[i], level+1, i)

        if isinstance(in_dict, list):
            for i in in_dict:
                dict_tree(i, level+1, parent)

    except:
        print "exception"
        return False

    return True


def dict_tree_map(in_dict, level=0, parent=""):
    """ map based implementation of the same """

    if not isinstance(in_dict, dict) and not isinstance(in_dict, list):
        return False

    try:
        if isinstance(in_dict, dict):
            tabs = "\t"*level
            print "-->{0} {1} {2}".format(tabs, str(parent), in_dict.keys())
            map(dict_tree_map, in_dict.values(),
                [level+1] * len(in_dict.values()), in_dict.keys())

        if isinstance(in_dict, list):
            map(dict_tree_map, in_dict,
                [level+1] * len(in_dict), [parent]*len(in_dict))

    except:
        print "exception"
        return False

    return True
