import random
from game_data import data_pusat
from features import fitur_survivor
from features import fitur_log
from features.fitur_achievement import check_achievements

# REKURSIF
# Traversal area
def recursive_area(current_area="Camp", visited=None, depth=0, indent=""):
    if visited is None:
        visited = set()
        print("\n" + "="*60)
        print("                     STRUKTUR AREA GAME")
        print("="*60)
        print("\n📌 Status Kunjungan Area (Tree View DFS)\n")

    visited.add(current_area)

    if current_area == "Camp":
        status_icon = "🏕️"
    else:
        status_icon = "🟢" if current_area in data_pusat.area_dikunjungi else "🔴"

    if depth == 0:
        print(f"🏕️  {current_area}")
    else:
        print(f"{indent}{current_area} {status_icon}")

    all_children = data_pusat.area_graph.get(current_area, [])
    
    if current_area == "Hutan":
        children = [c for c in all_children if c == "Kota Terbengkalai" and c not in visited]
    elif current_area == "Camp":
        children = [c for c in all_children if c in ["Hutan", "Sungai"] and c not in visited]
    else:
        children = [c for c in all_children if c not in visited]
    
    for i, next_area in enumerate(children):
        is_last = (i == len(children) - 1)

        if depth == 0:
            branch_symbol = "└── " if is_last else "├── "
        else:
            branch_symbol = "    └── " if is_last else "    ├── "
            
        recursive_area(next_area, visited, depth + 1, indent=indent.replace("├── ", "│   ").replace("└── ", "    ") + branch_symbol)

    if depth == 0:
        print("\n" + "-"*60)
        print("📋 DAFTAR AREA")

        fixed_order = [
            "Camp",
            "Hutan",
            "Kota Terbengkalai",
            "Sungai",
            "Gua"
        ]

        for area in fixed_order:
            if area == "Camp":
                print(f"- 🏕️  Camp")
            else:
                if area in data_pusat.area_dikunjungi:
                    print(f"- 🟢 {area}")
                else:
                    print(f"- 🔴 {area}")
        print("-"*60)
        print("🟢 = sudah dikunjungi")
        print("🔴 = belum dikunjungi")
        print("="*60)

# # EXPLORE AREA
# EXPLORE AREA
def explore_area():

    if not data_pusat.survivors:
        print("\nBelum ada survivor")
        return

    fitur_survivor.view_survivors()

    try:
        index = int(input("Pilih survivor: ")) - 1
        survivor = data_pusat.survivors[index]
    except:
        print("\nInput tidak valid")
        return

    # ENERGI BERDASARKAN EXPLORE HARI INI (RESET TIAP HARI)
    required_energy = (data_pusat.explore_count + 1) * 10
    if required_energy > 100:
        required_energy = 100

    print(f"\nEnergi yang dibutuhkan: {required_energy}")

    # Posisi awal survivor
    current_area = survivor.lokasi

    # Area yang terhubung dari posisi sekarang
    available_area = data_pusat.area_graph[current_area]

    print("\n================== AREA YANG BISA DIAKSES ==================")

    for area in available_area:
        print("-", area)

    print("============================================================")

    area_name = input("Pilih area: ").title()

    # Validasi area berdasarkan graph
    if area_name not in available_area:
        print("\nArea tidak ada dalam daftar yang bisa diakses")
        return

    if area_name not in data_pusat.data_area:
        print("\nArea tidak ditemukan")
        return

    key = survivor.nama.lower()

    # MATI KARENA SAKIT
    if key in data_pusat.sick_survivors:
        print(f"\n{survivor.nama} sedang sakit!")
        print(f"{survivor.nama} dipaksa eksplorasi...")
        print(f"💀 {survivor.nama} mati di perjalanan karena sakit")
        data_pusat.survivors.remove(survivor)
        data_pusat.sick_survivors.pop(key, None)
        fitur_log.add_single_log(f"{survivor.nama} meninggal saat eksplorasi karena sakit")
        fitur_log.add_double_log(f"{survivor.nama} meninggal saat eksplorasi karena sakit")
        return

    # MATI KARENA ENERGI
    if survivor.energi <= 0 or survivor.energi < required_energy:
        print(f"\n💀 {survivor.nama} mati karena energi tidak cukup")
        data_pusat.survivors.remove(survivor)
        data_pusat.sick_survivors.pop(key, None)
        fitur_log.add_single_log(f"{survivor.nama} meninggal karena kehabisan energi")
        fitur_log.add_double_log(f"{survivor.nama} meninggal karena kehabisan energi")
        return

    area = data_pusat.data_area[area_name]

    data_pusat.queue_eksplorasi.append(survivor.nama)
    print(f"\n{survivor.nama} masuk ke antrean eksplorasi")
    data_pusat.stack_eksplorasi.append(current_area)

    # BONUS JIKA AREA BARU PERTAMA KALI DIKUNJUNGI
    first_time = area.nama not in data_pusat.area_dikunjungi
    data_pusat.area_dikunjungi.add(area.nama)

    # Random resource
    found_resource = random.choice(area.sumber_daya)

    base_random = random.randint(1, 5)
    bonus_level = (survivor.level // 10) * 2

    base_amount = base_random + bonus_level

    bonus_camp = 0
    bonus_area = 0

    if data_pusat.camp_level >= 4:
        bonus_camp = 5

    # Bonus eksplorasi pertama kali
    if first_time:
        bonus_area = 5
        print(f"\n🌍 Area baru ditemukan! Bonus +5 {found_resource}")
    
    amount = base_amount + bonus_camp + bonus_area

    data_pusat.sumber_daya[found_resource] += amount

    # LEVEL SYSTEM FIX
    survivor.exp += 1

    need_exp = (survivor.level // 10) + 1

    if survivor.exp >= need_exp:
        survivor.level += 1
        survivor.exp = 0
        print(f"\nLevel Up! Sekarang level {survivor.level}")
    else:
        print(f"\nProgress Level: {survivor.exp}/{need_exp}")

    # KURANGI ENERGI
    survivor.energi -= required_energy

    # UPDATE LOKASI SURVIVOR
    survivor.lokasi = area_name

    # TAMBAH JUMLAH EXPLORE HARI INI
    data_pusat.explore_count += 1

    # LOG
    fitur_log.add_single_log(
        f"{survivor.nama} mengeksplor {area.nama} (+{amount} {found_resource})"
        )
    fitur_log.add_double_log(
        f"{survivor.nama} mengeksplor {area.nama} (+{amount} {found_resource})"
        )

    # HASIL
    print("\n===================== HASIL EKSPLORASI =====================")
    print(f"Survivor    : {survivor.nama}")
    print(f"Area        : {area.nama}")
    print(f"Mendapat    : +{base_amount} {found_resource}")
    if bonus_camp > 0:
        print(f"Bonus Camp  : +{bonus_camp} {found_resource}")
    if bonus_area > 0:
        print(f"Bonus Area  : +{bonus_area} {found_resource}")
    print(f"Total       : +{amount} {found_resource}")
    print(f"Energi      : -{required_energy}")
    print(f"Sisa Energi : {survivor.energi}")
    print(f"Level Up    : Level {survivor.level}")
    print("============================================================")

    if data_pusat.current_turn is None:
        data_pusat.current_turn = data_pusat.circular_head
    else:
        data_pusat.current_turn = data_pusat.current_turn.next
    
    check_achievements()

def backtrack_area():
    if not data_pusat.survivors:
        print("\nBelum ada survivor")
        return

    fitur_survivor.view_survivors()
    try:
        index = int(input("Pilih survivor yang mau ditarik mundur 1 langkah: ")) - 1
        survivor = data_pusat.survivors[index]
    except:
        print("\nInput tidak valid atau kosong!")
        return

    area_sekarang = survivor.lokasi

    if area_sekarang == "Camp":
        print(f"\n{survivor.nama} sudah berada di Camp, tidak bisa mundur lagi!")
        return

    if not data_pusat.stack_eksplorasi:
        area_sebelumnya = "Camp"
    else:
        area_sebelumnya = data_pusat.stack_eksplorasi.pop() 
        
        while area_sebelumnya == area_sekarang and data_pusat.stack_eksplorasi:
            area_sebelumnya = data_pusat.stack_eksplorasi.pop()
            
        if area_sebelumnya == area_sekarang:
            area_sebelumnya = "Camp"

    survivor.lokasi = area_sebelumnya
    
    print(f"\n[STACK POP - UNDO MOVEMENT]")
    print(f"Mundur dari : {area_sekarang}")
    print(f"Sekarang di : {survivor.lokasi}")
    print(f"{survivor.nama} berhasil mengambil satu langkah mundur!")
    fitur_log.add_single_log(f"{survivor.nama} backtrack dari {area_sekarang} ke {survivor.lokasi}")
    fitur_log.add_double_log(f"{survivor.nama} backtrack dari {area_sekarang} ke {survivor.lokasi}")

# PROCESS QUEUE
# Survivor yang masuk antrean akan diproses berdasarkan FIFO
def process_queue():

    print("\n" + "="*60)
    print("                  ANTREAN EKSPLORASI FIFO")
    print("="*60)

    if not data_pusat.queue_eksplorasi:
        print("❌ Tidak ada antrean eksplorasi")
        print("="*60)
        return

    print("\n📋 Daftar Antrean Saat Ini:")

    for i, nama in enumerate(data_pusat.queue_eksplorasi, start=1):
        print(f"{i}. {nama}")

    current = data_pusat.queue_eksplorasi.pop(0)

    print("\n" + "-"*60)
    print(f"🚶 Survivor Diproses : {current}")
    print("📌 Sistem Queue      : FIFO (First In First Out)")
    print("-"*60)

    if data_pusat.queue_eksplorasi:
        print("\n⏳ Antrean Berikutnya:")
        for i, nama in enumerate(data_pusat.queue_eksplorasi, start=1):
            print(f"{i}. {nama}")
    else:
        print("\n✅ Antrean eksplorasi sudah kosong")

    print("="*60)

def show_tree(tree, indent=""):

    if indent == "":
        print("\n" + "="*60)
        print("                     STRUKTUR AREA TREE")
        print("="*60)

    keys = list(tree.keys())

    for i, key in enumerate(keys):
        if indent == "":
            print("📍 " + key)
        else:
            connector = "└── " if i == len(keys)-1 else "├── "
            print(indent + connector + "📍 " + key)

        new_indent = indent + ("    " if i == len(keys)-1 else "│   ")

        if isinstance(tree[key], dict) and tree[key]:
            show_tree(tree[key], new_indent)

    if indent == "":
        print("="*60)