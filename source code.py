import pandas as pd
import time

class Node:
    def __init__(self, value):
        self.value = value   # (nim3, bb, nama)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def build_general_tree_from_excel(filename, max_children=3):
        df = pd.read_excel(filename)

        data = []
        for _, row in df.iterrows():
            nim3 = int(str(row["NIM"])[-3:])   # 3 digit terakhir NIM
            bb = row["BB"]                    # berat badan
            nama = row["Nama Lengkap"]
            data.append((nim3, bb, nama))

        root = Node(data[0])
        queue = [root]
        idx = 1

        while idx < len(data):
            parent = queue.pop(0)
            for _ in range(max_children):
                if idx < len(data):
                    child = Node(data[idx])
                    parent.add_child(child)
                    queue.append(child)
                    idx += 1
        return root



def flatten_tree(root):
    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.value)
        for c in reversed(node.children):
            stack.append(c)
    return result




def is_greater(a, b):
    # a dan b berbentuk (nim3, bb, nama)
    # prioritas: BB → NIM → Nama
    return (a[1], a[0], a[2]) > (b[1], b[0], b[2])



def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if is_greater(a[j], a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
    return a



def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and is_greater(a[j], key):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a



def quick_sort(arr):
    a = arr[:]

    def _quick(low, high):
        if low < high:
            p = partition(low, high)
            _quick(low, p - 1)
            _quick(p + 1, high)

    def partition(low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            if not is_greater(a[j], pivot):
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[high] = a[high], a[i + 1]
        return i + 1

    _quick(0, len(a) - 1)
    return a



def benchmark(func, data):
    start = time.time()
    result = func(data)
    end = time.time()
    return result, end - start



filename = "Copy of Kelas_70 revisi II.xlsx"

root = Node.build_general_tree_from_excel(filename, max_children=3)
data_flat = flatten_tree(root)

bubble_res, t1 = benchmark(bubble_sort, data_flat)
insertion_res, t2 = benchmark(insertion_sort, data_flat)
quick_res, t3 = benchmark(quick_sort, data_flat)



def print_data(title, data):
    print(f"\n=== {title} ===")
    for nim, bb, nama in data:
        print(f"NIM: {nim} | BB: {bb} | Nama: {nama}")

print_data("Hasil Bubble Sort (BB Terkecil)", bubble_res)
print_data("Hasil Insertion Sort (BB Terkecil)", insertion_res)
print_data("Hasil Quick Sort (BB Terkecil)", quick_res)

print("\n=== WAKTU EKSEKUSI ===")
print(f"Bubble Sort    : {t1:.6f} detik")
print(f"Insertion Sort : {t2:.6f} detik")
print(f"Quick Sort     : {t3:.6f} detik")
