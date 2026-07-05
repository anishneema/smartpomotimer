# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:

        ans = float('-inf')
        
        def bestPath(node):
            nonlocal ans

            if node is None:
                return 0

            max_left = bestPath(node.left)
            max_right = bestPath(node.right)

            ans = max(ans, max(max_left, 0) + node.val + max(max_right,0))

            return node.val + max(0,max_left,max_right)
        
        bestPath(root)
        return ans