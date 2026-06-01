from game_data import data_pusat
from structures.struktur_node import SingleNode, DoubleNode, CircularNode

# SINGLE LINKED LIST
# Menambahkan activity log
def add_single_log(text):
    new_node = SingleNode(text)

    if data_pusat.log_head is None:
        data_pusat.log_head = new_node
    else:
        current = data_pusat.log_head

        while current.next:
            current = current.next

        current.next = new_node

# Menampilkan activity log
def show_single_log():

    current = data_pusat.log_head

    print("\n" + "="*60)
    print("                     ACTIVITY TIMELINE")
    print("="*60)

    if current is None:
        print("\n❌ Belum ada aktivitas")
        print()
        print("="*60)
        return

    nomor = 1

    while current:
        kolom_nomor = f"[{nomor}]"
        print(f"\n{kolom_nomor:<6} 🔹 {current.data}")
        print()
        print("        │")
        current = current.next
        nomor += 1

    print("\n" + "="*60)
    print(f"📌 Total Aktivitas Tercatat : {nomor - 1}")
    print("="*60)

# DOUBLE LINKED LIST
# Menambahkan log ke double linked list
def add_double_log(text):
    new_node = DoubleNode(text)

    if data_pusat.double_head is None:
        data_pusat.double_head = data_pusat.double_tail = new_node
    else:
        data_pusat.double_tail.next = new_node
        new_node.prev = data_pusat.double_tail
        data_pusat.double_tail = new_node

# Menampilkan log dari depan
def show_double_forward():

    current = data_pusat.double_head

    print("\n" + "="*60)
    print("                 DOUBLE LINKED LIST FORWARD")
    print("="*60)

    if current is None:
        print("\n❌ Belum ada data log")
        print()
        print("="*60)
        return

    nomor = 1

    while current:

        prev_data = current.prev.data if current.prev else "None"
        next_data = current.next.data if current.next else "None"

        print(f"\n[{nomor}] 📌 {current.data}")
        print(f"     ⬅️  Prev : {prev_data}")
        print(f"     ➡️  Next : {next_data}")

        if current.next:
            print()
            print("     │")
            print("     ▼")

        current = current.next
        nomor += 1

    print("\n" + "="*60)
    print(f"📋 Total Node : {nomor - 1}")
    print("📌 Traversal : HEAD ➜ TAIL")
    print("="*60)

# Menampilkan log dari belakang
def show_double_backward():

    current = data_pusat.double_tail

    print("\n" + "="*60)
    print("                DOUBLE LINKED LIST BACKWARD")
    print("="*60)

    if current is None:
        print("\n❌ Belum ada data log")
        print()
        print("="*60)
        return

    nomor = 1

    while current:

        prev_data = current.prev.data if current.prev else "None"
        next_data = current.next.data if current.next else "None"

        print(f"\n[{nomor}] 📌 {current.data}")
        print(f"     ⬅️  Prev : {prev_data}")
        print(f"     ➡️  Next : {next_data}")

        if current.prev:
            print()
            print("     ▲")
            print("     │")

        current = current.prev
        nomor += 1

    print("\n" + "="*60)
    print(f"📋 Total Node : {nomor - 1}")
    print("📌 Traversal : TAIL ➜ HEAD")
    print("="*60)

# CIRCULAR LINKED LIST
# Menambahkan survivor ke circular list
def add_circular_survivor(survivor):
    new_node = CircularNode(survivor)

    if data_pusat.circular_head is None:
        data_pusat.circular_head = new_node
        new_node.next = new_node
    else:
        current = data_pusat.circular_head

        while current.next != data_pusat.circular_head:
            current = current.next

        current.next = new_node
        new_node.next = data_pusat.circular_head

# Menampilkan giliran survivor
def show_circular_survivor():

    if data_pusat.circular_head is None:
        print("\n❌ Belum ada Survivor")
        return

    print("\n" + "="*60)
    print("                  ROTASI GILIRAN SURVIVOR")
    print("="*60)

    current = data_pusat.circular_head
    nomor = 1
    print()
    while True:

        status = ""

        if data_pusat.current_turn == current:
            status = "  [GILIRAN SEKARANG]"

        print(f"{nomor}. {current.survivor.nama}{status}")

        current = current.next
        nomor += 1

        if current == data_pusat.circular_head:
            break

    print("\n📌 Sistem menggunakan Circular Linked List")
    print()
    print("="*60)

#Sistem survivor turn rotation
def next_turn():

    if data_pusat.circular_head is None:
        print("\n❌ Belum ada survivor")
        return

    if data_pusat.current_turn is None:
        data_pusat.current_turn = data_pusat.circular_head

    current = data_pusat.current_turn.survivor

    print("\n" + "="*60)
    print("                      GILIRAN SURVIVOR")
    print("="*60)

    print(f"\n👤 Nama   : {current.nama}")
    print(f"⚡ Energi : {current.energi}")
    print(f"⭐ Level  : {current.level}")
    print(f"📍 Lokasi : {current.lokasi}")

    print("\n🔄 Sistem rotasi circular aktif")
    print()
    print("="*60)

