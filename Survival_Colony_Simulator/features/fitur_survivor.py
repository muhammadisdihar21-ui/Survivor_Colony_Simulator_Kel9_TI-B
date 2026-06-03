from game_data import data_pusat
from features.fitur_achievement import check_achievements
from models.komponen_game import Survivor
from features import fitur_log

# MENAMBAHKAN SURVIVOR
def add_survivor():
    nama = input("Masukkan nama survivor: ").strip()

    if not nama:
        print("\nNama tidak boleh kosong")
        return
        
    if len(nama) > 30:
        print("\nNama terlalu panjang! Maks 30 karakter")
        return
        
    for s in data_pusat.survivors:
        if s.nama.lower() == nama.lower():
            print("\nNama survivor sudah ada")
            return
            
    survivor = Survivor(nama)

    data_pusat.survivors.append(survivor)

    data_pusat.total_survivor_created += 1

    if len(data_pusat.survivors) > data_pusat.max_survivor_reached:
        data_pusat.max_survivor_reached = len(data_pusat.survivors)

    # Menambahkan survivor ke circular linked list
    fitur_log.add_circular_survivor(survivor)

    # Menambahkan log
    fitur_log.add_single_log(f"{nama} bergabung ke koloni")
    fitur_log.add_double_log(f"{nama} bergabung ke koloni")

    print("\nSurvivor berhasil ditambahkan")

    check_achievements()

# MENAMPILKAN SURVIVOR
def view_survivors():
    if not data_pusat.survivors:
        print("\nBelum ada Survivor")
        return

    print("\n===================== DAFTAR SURVIVOR ======================")

    for i, s in enumerate(data_pusat.survivors, start=1):
        status = " [SAKIT]" if s.nama.lower() in data_pusat.sick_survivors else ""
        print(f"{i}. {s.nama}{status}")
        print(f"   Energi : {s.energi}")
        print(f"   Level  : {s.level}")
        print("------------------------------------------------------------")

# SEARCHING SURVIVOR
def search_survivor():
    keyword = input("Masukkan nama survivor: ").lower()

    found = False

    for s in data_pusat.survivors:
        if s.nama.lower() == keyword:
            print("\n==================== SURVIVOR DITEMUKAN ====================")
            print(f"Nama   : {s.nama}")
            print(f"Energi : {s.energi}")
            print(f"Level  : {s.level}")
            print("============================================================")
            found = True

    if not found:
        print("\nSurvivor tidak ditemukan")

# MERGE SORT
def merge_sort_survivor(arr, choice):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort_survivor(arr[:mid], choice)
    right = merge_sort_survivor(arr[mid:], choice)

    return merge(left, right, choice)


def merge(left, right, choice):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if choice == "1":  # Energi

            if left[i].energi >= right[j].energi:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        elif choice == "2":  # Level

            if left[i].level >= right[j].level:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# SORTING SURVIVOR
def sort_survivors():

    if not data_pusat.survivors:
        print("\nBelum ada survivor")
        return
    
    print()
    print("1. Urutkan berdasarkan Energi")
    print("2. Urutkan berdasarkan Level")

    choice = input("Pilih: ")

    if choice == "1":
        kategori = "ENERGI"
    elif choice == "2":
        kategori = "LEVEL "
    else:
        print("\nPilihan tidak valid")
        return

    sorted_list = merge_sort_survivor(data_pusat.survivors[:], choice)

    print(f"\n============= DATA SURVIVOR BERDASARKAN {kategori} =============")
    print("------------------------------------------------------------")
    print(f"{'No':<5}{'Nama':<36}{'Energi':^10}{'Level':^12}")
    print("------------------------------------------------------------")

    for i, s in enumerate(sorted_list, start=1):
        print(f"{str(i) + '.':<5}{s.nama:<36}{str(s.energi):^10}{str(s.level):^12}")

    print("------------------------------------------------------------")

# MENGHAPUS SURVIVOR
def delete_survivor():
    nama = input("Masukkan nama survivor: ")

    for s in data_pusat.survivors:
        if s.nama.lower() == nama.lower():
            data_pusat.survivors.remove(s)
            data_pusat.total_survivor_dead += 1
            if len(data_pusat.survivors) < data_pusat.min_survivor_reached:
                data_pusat.min_survivor_reached = len(data_pusat.survivors)
            data_pusat.sick_survivors.pop(s.nama.lower(), None)

            data_pusat.circular_head = None
            for surv in data_pusat.survivors:
                fitur_log.add_circular_survivor(surv)

            fitur_log.add_single_log(f"{nama} dihapus")
            fitur_log.add_double_log(f"{nama} dihapus")

            print("\nSurvivor berhasil dihapus")
            return

    print("\nSurvivor tidak ditemukan")

    check_achievements()