"""
File: linkedbst.py
Author: Ken Lambert
"""
import time
from random import choice
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """
        Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present.
        >>> len(LinkedBST([12]))
        1
        """
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)


    def __iter__(self):
        """
        Supports a preorder traversal on a view of self.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.__iter__().__next__()
        123
        """
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """
        Supports a preorder traversal on a view of self.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.add(234)
        >>> tree.add(12)
        >>> tree.preorder().__next__()
        123
        """
        nodes_lst = [self._root]
        nodes_data = []
        while len(nodes_lst) != 0:
            cur_node = nodes_lst[0]
            if cur_node:
                nodes_data.append(cur_node.data)
                nodes_lst += [cur_node.left,cur_node.right]
            nodes_lst.remove(cur_node)

        return iter(nodes_data)


    def __contains__(self, item):
        """
        Returns True if target is found or False otherwise.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> 123 in tree
        True
        """
        return self.find(item) != None

    def find(self, item):
        """
        If item matches an item in self, returns the
        matched item, or None otherwise.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.add(34)
        >>> tree.find(123).data
        123
        """

        if self.isEmpty():
            return None
        cur_node = self._root
        while cur_node != None:
            if cur_node.data == item:
                return cur_node
            if cur_node.data < item:
                cur_node = cur_node.right
            elif cur_node.data > item:
                cur_node = cur_node.left
            continue

    # Mutator methods
    def clear(self):
        """
        Makes self become empty.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.add(34)
        >>> tree.clear()
        >>> tree._root
        """
        self._root = None
        self._size = 0

    def add(self, item):
        """
        Adds item to the tree.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree._root.data
        123
        """
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            cur_node = self._root
            while True:
                if not cur_node:
                    cur_node = BSTNode(item)
                    break
                if cur_node.data < item:
                    if not cur_node.right:
                        cur_node.right = BSTNode(item)
                        break
                    else:
                        cur_node = cur_node.right
                elif cur_node.data > item:
                    if not cur_node.left:
                        cur_node.left = BSTNode(item)
                        break
                    else:
                        cur_node = cur_node.left
                continue
        self._size += 1


    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.replace(123,'Hello')
        123
        >>> 'Hello' in tree
        True
        """
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None


    def range_find(self, low, high):
        '''
        Returns a list of the items in the 
        tree, where low <= item <= high
        :param low:
        :param high:
        :return:
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.add(34)
        >>> tree.add(11)
        >>> tree.add(678)
        >>> tree.add(100)
        >>> tree.range_find(11, 112)
        [34, 11, 100]
        '''
        result_items = []
        for node in self.preorder():
            if low <= node <= high:
                result_items.append(node)
        return result_items


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        >>> tree = LinkedBST()
        >>> tree.add(123)
        >>> tree.add(34)
        >>> tree.add(11)
        >>> tree.add(678)
        >>> tree.add(100)
        >>> tree.rebalance()
        >>> tree._root.data
        100
        '''
        nodes = []
        for child in self.preorder():
            nodes.append(child)
        self._size =  0
        nodes.sort()
        nodes_parts = [nodes]
        while len(nodes_parts) != 0:
            temp_parts = []
            for part in nodes_parts:
                if len(part) > 1:
                    results = self.add_rebalance(part)
                    temp_parts += results[:2]
                    self.add(results[2])
                elif len(part) == 1:
                    self.add(part[0])
            nodes_parts = temp_parts.copy()
            temp_parts.clear()

    @staticmethod
    def add_rebalance(nodes_lst):
        mid = int(len(nodes_lst)/2)
        part_1 = nodes_lst[:mid]
        part_2 = nodes_lst[mid+1:]
        return [part_1,part_2,nodes_lst[mid]]


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        >>> tree = LinkedBST()
        >>> tree.add(11)
        >>> tree.add(678)
        >>> tree.add(100)
        >>> tree.successor(90).data
        100
        """
        if self.isEmpty():
            return None
        start_node = self.find(item)
        if start_node and start_node.right:
            return start_node.right
        min_node = None
        for node in self.preorder():
            if node > item:
                if min_node == None:
                    min_node = BSTNode(node)
                elif node <= min_node.data:
                    min_node = BSTNode(node)
        if min_node != None:
            return min_node
        return None


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        >>> tree = LinkedBST()
        >>> tree.add(11)
        >>> tree.add(678)
        >>> tree.add(100)
        >>> tree.add(9)
        >>> tree.predecessor(11).data
        9
        """
        start_node = self.find(item)
        if self.isEmpty() or not start_node:
            return None
        if start_node.left != None:
            return start_node.left
        return None


    def demo_bst(self, path:str) -> tuple:
        """
        Demonstration of efficiency binary
        search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_list = []
        search_word,counter = [],0
        file_data = open(path,'r',encoding='utf-8')
        for word in file_data:
            word = word.strip()
            if word != '':
                self.add(word)
                words_list.append(word+'\n')
        indexes = [i for i in range(len(words_list))]
        while counter != 10000:
            idx = choice(indexes)
            search_obj = words_list[idx]
            if search_obj not in search_word:
                search_word.append(search_obj)
                counter += 1
        time_1 = self.demo_bst_1(search_word,words_list)
        time_2 = self.demo_bst_2(search_word)
        time_3 = self.demo_bst_3(search_word,words_list)
        time_4 = self.demo_bst_4(search_word)
        return time_1,time_2,time_3,time_4


    def demo_bst_3(self, search_words:list, data_lst:list) -> int:
        '''
        Searches words in binary tree.
        Words are not in the alphabetic order.
        Returns the search time.
        '''
        self._root = None
        while len(data_lst) != 0:
            word = choice(data_lst)
            self.add(word)
            data_lst.remove(word)
        st_time = time.time()
        self.preorder()
        for word in search_words:
            self.find(word)
        return time.time() - st_time


    def demo_bst_4(self, search_words:list) -> int:
        '''
        Searches words in balanced binary tree.
        Words are not in the alphabetic order.
        Returns the search time.
        '''
        self.rebalance()
        start_time = time.time()
        for word in search_words:
            self.find(word)
        return round(time.time() - start_time,8)


    def demo_bst_2(self, search_words:list) -> int:
        '''
        Searches words in binary tree.
        Words are in the alphabetic order.
        Returns the search time.
        '''
        start_time = time.time()
        for word in search_words:
            self.find(word)
        return time.time() - start_time


    @staticmethod
    def demo_bst_1(search_lst,data:list) -> int:
        '''
        Searches words in the list.
        Words are in the alphabetic order.
        Returns search time.
        '''
        start_time = time.time()
        for word in search_lst:
            data.index(word)
        return time.time() - start_time
