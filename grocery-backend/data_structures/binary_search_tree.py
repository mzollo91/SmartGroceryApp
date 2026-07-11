class TreeNode:
	def __init__(self, value):
		self.value = value
		self.left = None # Points to another node
		self.right = None # Same as above
		
class BinarySearchTree:
	def __init__(self):
		self.root = None
		
	def insert(self, value):
		# Case 1, the tree is empty.
		# The node then becomes the root
		if self.root is None:
			self.root = TreeNode(value)
		else:
			# Case 2, the tree is not empty.
			# Hand this off to the recursive engine.
			# Search starts at the top.
			self._insert_recursive(self.root, value)
			
	def _insert_recursive(self, current_node, value):
		# Private helper to find the right spot.
			
		# Look left if the value is smaller
		#  than the current node value.
		if value < current_node.value:
			# If the left slot is empty, end recursion.
			if current_node.left is None:
				current_node.left = TreeNode(value)
			else:
				# If occupied, then repeat recursion.
				self._insert_recursive(current_node.left, value)
		
		# If value is greater, go to the right			
		if value > current_node.value:
			# Same procedure as going left.
			if current_node.right is None:
				current_node.right = TreeNode(value)
			else:
				self._insert_recursive(current_node.right, value)
					
		# As a general note, if the value ==
		# current_node.value, do nothing.
		# BSTs ignore duplicate values.
		
	def contains(self, value):
		# Returns True if found, else false
		return self._contains_recursive(self.root, value)
	
	def _contains_recursive(self, current_node, value):
		# Base case #1, dead end. The value
		# is not in the tree.
		if current_node is None:
			return False
			
		# Base case #2, the value is found.
		if current_node.value == value:
			return True
			
		# Recursive case #1,
		# if value is smaller than current node
		# go to the left
		if value < current_node.value:
			return self._contains_recursive(current_node.left, value)
			
		# Conversely, go to the right if
		# value > current node.
		return self._contains_recursive(current_node.right, value)
		
	def in_order_traversal(self):
		
		# Base case #1, an empty tree.
		if self.root is None:
			print("Empty Tree")
		else:
			self._iot_recursive(self.root)
			
	def _iot_recursive(self, current_node):
		
		# Check if node does not exist, exit recursion.
		# This allows the code to run unconditionally,
		# meaning fewer if statements.
		if current_node is None:
			return
	
		self._iot_recursive(current_node.left)
		print(current_node.value)
		self._iot_recursive(current_node.right)
		
	def find_min(self):
		# Walk left down the tree until the
		# smallest value is obtained.
		
		if self.root is None:
			return None
			
		current = self.root
		
		# Ride the left side down until the end.
		while current.left is not None:
			current = current.left
			
		return current.value
		
	def find_max(self):
		# Walk right down the tree until the
		# largest value is obtained.
		
		if self.root is None:
			return None
			
		current = self.root
		
		# Ride the right side down until the end.
		while current.right is not None:
			current = current.right
			
		return current.value
		
	def get_tree_height(self):
		# Public function to get height of tree.
		return self._get_height_recursive(self.root)
		
	def _get_height_recursive(self, current_node):
		# Start with base case of empty node.
		if current_node is None:
			return -1
			
		left_height = self._get_height_recursive(current_node.left)
		right_height = self._get_height_recursive(current_node.right)
		
		return 1 + max(left_height, right_height)
		
	def delete_node(self, value):
		self.root = self._delete_recursive(self.root, value)
		
	def _delete_recursive(self, current_node, value):
		# Base case, dead end. Value not found.
		if current_node is None:
			return current_node
		
		# If the value is less than the node, go left.	
		if value < current_node.value:
			current_node.left = self._delete_recursive(current_node.left, value)
		
		# If the value is greater than the node
		# go right.
		elif value > current_node.value:
			current_node.right = self._delete_recursive(current_node.right, value)
			
		# If value is found, begin deletion.
		else:
			# This covers case 1 and 2; no children
			# or just one child. If a child node is none,
			# return the other side. If no child exists,
			# None is returned. If only one child exists
			# The parent node is redirected to the
			# the existing child.
			if current_node.left is None:
				return current_node.right
			if current_node.right is None:
				return current_node.left
				
			# Next case, the node has 2 children.
			# Find the min value of the right subtree.
			successor = current_node.right
			while successor.left is not None:
				successor = successor.left
				
			# This is the minimum value in the
			# right subtree. As such, it is guaranteed
			# to not have a left child.
			current_node.value = successor.value
			current_node.right = self._delete_recursive(current_node.right, successor.value)
		return current_node