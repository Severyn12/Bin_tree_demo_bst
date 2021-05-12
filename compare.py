'''This module  compares search time'''
from bin_tree import LinkedBST

bin_tree = LinkedBST()
times = bin_tree.demo_bst('words.txt')
print('Words are in the alphabetic order\n')
print(f'Search time of 10 000 words in list: {times[0]}\n')
print(f'Search time of 10 000 words in bin tree: {times[1]}\n')
print('Words are not in the alphabetic order\n')
print(f'Search time of 10 000 words in bin tree: {times[2]}\n')
print(f'Search time of 10 000 words in balanced bin tree: {times[3]}\n')


