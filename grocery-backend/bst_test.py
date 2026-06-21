from binary_search_tree import BinarySearchTree

bst = BinarySearchTree()
bst.insert(10)
bst.insert(5)
bst.insert(15)

# Checking if pointers are mapped correctly
if bst.root is not None:
    print(f"Root: {bst.root.value}")          # Should be 10
    if bst.root.left is not None:
        print(f"Left Child: {bst.root.left.value}") # Should be 5
    if bst.root.right is not None:
        print(f"Right Child: {bst.root.right.value}") # Should be 15
			
# Setup your test tree
bst = BinarySearchTree()
for num in [50, 40, 70, 30, 60, 61, 82, 43, 71]:
    bst.insert(num)

# Test Lookups
print(bst.contains(60))  # Should print: True
print(bst.contains(65))  # Should print: False (Hits None under 60)
print(bst.contains(40))
print(bst.contains(70))

bst.in_order_traversal()
print(f"The min of the tree: {bst.find_min()}")
print(f"The max of the tree: {bst.find_max()}")
print(f"The height of the tree: {bst.get_tree_height()}")
bst.delete_node(60)
bst.in_order_traversal()