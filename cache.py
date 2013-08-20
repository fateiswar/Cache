+import sys
+import time
+import threading
+import heapq
+
+class Lock(object):
+    def __init__(self, lock):
+	self._lock = lock
+
+    def __enter__(self):
+	self._lock.acquire()
+
+    def __exit__(self):
+	self._lock.release()
+
+class Cache:
+    def __init__(self, maxsize, expire_time):
+	self.maxsize = maxsize
+	self.lock = threading.Lock()
+	self.expire_time = expire_time
+	self.mp = {} #mp<key, (val, time)>
+	self.pq = [] #pq[(time, key)]
+
+    def get(self, key):
+	lock = Lock(self.lock)
+	if self.mp.has_key(key):
+	    val = self.mp[key]
+	    if val[1] + self.expire_time < time.time():
+		return None
+	    return val[0]
+	return None
+
+    def upd(self):
+	if len(self.pq) < self.maxsize:
+	    return
+	while true:
+	    top = heapq.heappop(self.pq)
+	    val = self.mp[top[1]]
+	    if top[0] != val[1]:
+		heapq.heappush(self.pq, (val[1], top[1]))
+	    else:
+		del self.mp[top[1]]
+		break
+
+    def put(self, key, val):
+	lock = Lock(self.lock)
+	if self.mp.has_key(key):
+	    self.mp[key] = (val, time.time())
+	else:
+	    self.upd()
+	    curr_time = time.time()
+	    self.mp[key] = (val, curr_time)
+	    heapq.heappush(self.pq, (curr_time, key))
