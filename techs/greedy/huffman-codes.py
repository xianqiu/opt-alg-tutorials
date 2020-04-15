import queue


class Node(object):

    def __init__(self):
        # data
        self.char = None  # character
        self.freq = None  # frequency
        # pointers
        self.left = None  # left child
        self.right = None  # right child


class HuffmanCodes(object):

    def __init__(self, c, f):
        """
        :param c: characters, str list
        :param f: frequencies, int list
        """
        self._c = c
        self._f = f
        self._n = len(self._c)
        self._q = self._init_priority_queue()
        self._root = None  # encoding tree
        self._huffman_codes = {}  # 编码结果
        self._build_binary_tree() # 构建二叉树
        self._format_huffman_codes()  # 保存编码结果

    def _init_priority_queue(self):
        """ 初始化优先队列.
        priority = frequency, value = node
        使用优先队列可以在O(log n)内返回队列的最小值(代价是插入元素的耗时为O(log n)).
        """
        q = queue.PriorityQueue()
        for item in zip(self._c, self._f):
            v = Node()
            v.char, v.freq = item[0], item[1]
            q.put((v.freq, v))
        return q

    def _build_binary_tree(self):
        """ 自下而上构建二叉树.
        Greedy: 每一步从未被连接的节点中, 选择频次(frequency)最小的两个节点合并(作为新的节点).
        """
        for i in range(self._n - 1):
            z = Node()
            # 从队列里弹出两个最小权重的节点,合并成新的节点z
            z.left = self._q.get()[1]
            z.right = self._q.get()[1]
            z.freq = z.left.freq + z.right.freq
            # 把z插入到队列中
            self._q.put((z.freq, z))
        # 执行n-1步之后, 队列q剩下一个元素,即二叉树的根节点.
        self._root = self._q.get()[1]

    def _format_huffman_codes(self):
        """ 把每一个字符对应的编码保存在字典中(self._huffman_codes)
   		"""
        temp = []

        def traverse(v, res):
            if v.left is None and v.right is None:
                self._huffman_codes[v.char] = ''.join(res)
                return
            res.append('0')
            traverse(v.left, res)
            res.pop(-1)
            res.append('1')
            traverse(v.right, res)
            res.pop(-1)

        traverse(self._root, temp)

    def encode(self, chars):
        """ 把字符串chars转换成Huffman codes.
        """
        return ''.join([self._huffman_codes[c] for c in chars])

    def decode(self, codes):
        """ 把0/1编码(字符串格式)转换成字符串.
        """
        res = []
        v = self._root
        for c in codes:
            if c == '0':
                v = v.left
            elif c == '1':
                v = v.right
            if v.left is None and v.right is None:
                res.append(v.char)
                v = self._root

        return ''.join(res)


if __name__ == '__main__':

    hc = HuffmanCodes(['a', 'b', 'c', 'd', 'e', 'f'], [45, 13, 12, 16, 9, 5])
    print('==== Huffman encoding ====')
    string = 'acdefcbe'
    codes = hc.encode(string)
    print("%s -> %s" % (string, codes))
    print('==== Huffman decoding ====')
    print('%s -> %s' % (codes, hc.decode(codes)))
