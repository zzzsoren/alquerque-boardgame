from dataclasses import dataclass

@dataclass
class Item:
    prev: None
    next: None
    node: None
    value: int

@dataclass
class Queue:
    first: None
    last: None
    size: int

def make_queue() -> Queue:
    return Queue(None, None, 0)

def size(q: Queue) -> int:
    return q.size

def has_next(q: Queue) -> bool:
    return q.first is not None

def next(q: Queue) -> int:
    item = q.first
    q.first = q.first.next
    if q.first is not None:
        q.first.prev = None
    else:
        q.last = None
    q.size = q.size-1
    return item.node

def add(q: Queue, node: None, value: int) -> None:
    if q.size == 0:
        q.first = Item(None, None, node, value)
        q.last = q.first
    else:
        n = q.last
        while n is not None and value > n.value:
            n = n.prev      
        if n is None:
            q.first = Item(None, q.first, node, value)
            q.first.next.prev = q.first
        else:
            n.next = Item(n, n.next, node, value)
            if n.next.next is None:
                q.last = n.next
            else:
                n.next.next.prev = n.next
    q.size = q.size+1

