import json
import random
from game_data import data_pusat
from features import fitur_survivor
from features import fitur_log
from features.fitur_achievement import check_achievements
from models.komponen_game import Survivor

# MENAMPILKAN RESOURCE
def show_resources():
    print("\n==================== SUMBER DAYA KOLONI ====================")

    for key, value in data_pusat.sumber_daya.items():
        print(f"{key:<10}: {value}")

    print("============================================================")

# MAKANAN
# Fungsi untuk memberikan makanan kepada survivor
def eat_food():
    if not data_pusat.survivors:
        print("\nBelum ada survivor")
        return
        
    fitur_survivor.view_survivors()

    try:
        index = int(input("Pilih survivor: ")) - 1
        if index < 0 or index >= len(data_pusat.survivors):
            print("\nNomor survivor tidak valid")
            return
        survivor = data_pusat.survivors[index]
    except ValueError:
        print("\nInput harus berupa angka")
        return
        
    # Survivor yang sakit tidak bisa makan
    if survivor.nama.lower() in data_pusat.sick_survivors:
        print(f"\n{survivor.nama} sedang sakit!")
        print("Tidak bisa diberi makan sebelum disembuhkan")
        return
        
    try:
        amount = int(input("Jumlah makanan: "))
    except:
        print("\nInput tidak valid")
        return
        
    if amount <= 0:
        print("\nJumlah makanan harus lebih dari 0")
        return
        
    if data_pusat.sumber_daya["Makanan"] < amount:
        print("\nMakanan tidak cukup")
        return
        
    data_pusat.sumber_daya["Makanan"] -= amount
    survivor.energi += amount * 10

    if survivor.energi > 100:
        survivor.energi = 100
        
    print(f"\n{survivor.nama} mendapatkan +{amount * 10} energi")
    fitur_log.add_single_log(f"{survivor.nama} diberi {amount} Makanan (+{amount * 10} Energi)")
    fitur_log.add_double_log(f"{survivor.nama} diberi {amount} Makanan (+{amount * 10} Energi)")

# SCALING COST BERDASARKAN HARI
def get_event_cost():
    cost = 5 + ((data_pusat.hari - 1) // 10) * 5

    if cost > 100:
        cost = 100
    
    return cost

# REPAIR CAMP
# Fungsi untuk memperbaiki camp
def repair_camp():
    if not data_pusat.camp_damaged:
        print("\nCamp tidak rusak")
        return
        
    repair_cost = get_event_cost()

    if data_pusat.sumber_daya["Material"] < repair_cost:
        print(f"\nMaterial tidak cukup (Butuh {repair_cost} Material)")
        return
        
    data_pusat.sumber_daya["Material"] -= repair_cost
    data_pusat.camp_damaged = False
    print(f"\nCamp berhasil diperbaiki dengan biaya {repair_cost} Material")

    fitur_log.add_single_log(f"Camp diperbaiki ({repair_cost} Material digunakan)")

    fitur_log.add_double_log(f"Camp diperbaiki ({repair_cost} Material digunakan)")

# HEAL SURVIVOR
# Fungsi mengobati survivor yang sakit
def heal_survivor():
    if not data_pusat.sick_survivors:
        print("\nTidak ada survivor yang sakit")
        return
        
    print("\n====================== SURVIVOR SAKIT ======================")

    for name in data_pusat.sick_survivors:
        print("-", name)

    print("============================================================")

    name = input("Masukkan nama survivor: ").strip().lower()

    if not name:
        print("\nInput tidak boleh kosong")
        return

    survivor_exists = any(s.nama.lower() == name for s in data_pusat.survivors)

    if not survivor_exists:
        print("\nSurvivor ini tidak ada dalam koloni")
        return

    if name not in data_pusat.sick_survivors:
        print("\nSurvivor ini tidak sedang sakit")
        return
        
    medicine_cost = get_event_cost()

    if data_pusat.sumber_daya["Obat"] < medicine_cost:
        print(f"\nObat tidak cukup (Butuh {medicine_cost} Obat)")
        return
        
    data_pusat.sumber_daya["Obat"] -= medicine_cost
    del data_pusat.sick_survivors[name]

    for s in data_pusat.survivors:
        if s.nama.lower() == name:
            s.energi = 10
            break
        
    print(f"\n{name} berhasil sembuh dengan biaya {medicine_cost} Obat")
    print("Energi rendah, beri makanan untuk menambah energi")

    fitur_log.add_single_log(f"{name} sembuh dari penyakit ({medicine_cost} Obat digunakan)")

    fitur_log.add_double_log(f"{name} sembuh dari penyakit ({medicine_cost} Obat digunakan)")
    
# INFO UPGRADE
def show_upgrade_info():

    next_level = data_pusat.camp_level + 1

    print("\n==================== INFO UPGRADE CAMP =====================")
    print(f"Level Camp Saat Ini: {data_pusat.camp_level}")

    if next_level > 5:
        print("Camp sudah level maksimum (Lv5)")
        print("============================================================")
        return

    print(f"\nKeuntungan Upgrade ke Level {next_level}:")

    if next_level == 2:
        print("- Rest energy +20 (50 → 70)")
    
    elif next_level == 3:
        print("- Event lebih aman (lebih sering tidak terjadi apa-apa / food event)")

    elif next_level == 4:
        print("- Bonus eksplorasi +5 resource")

    elif next_level == 5:
        print("- Unlock Achievement System")

    print(f"\nUntuk Upgrade ke Level {next_level} Membutuhkan:")

    if next_level == 2:
        print("- 20 Makanan")
        print("- 20 Material")
        print("- 5 Obat")
        print("- Minimal 1 survivor level 10")

    elif next_level == 3:
        print("- 30 Makanan")
        print("- 30 Material")
        print("- 10 Obat")
        print("- Minimal 1 survivor level 20")

    elif next_level == 4:
        print("- 40 Makanan")
        print("- 40 Material")
        print("- 20 Obat")
        print("- Minimal 2 survivor level 30")

    elif next_level == 5:
        print("- 80 Makanan")
        print("- 80 Material")
        print("- 50 Obat")
        print("- Minimal 1 survivor level 100")

    print("============================================================")

# CEK UPGRADE
def check_upgrade():

    next_level = data_pusat.camp_level + 1

    if next_level > 5:
        print("\nCamp sudah level maksimum")
        return False

    kurang = []

    # RESOURCE CHECK
    if next_level == 2:
        if data_pusat.sumber_daya["Makanan"] < 20:
            kurang.append("Makanan kurang (butuh 20)")
        if data_pusat.sumber_daya["Material"] < 20:
            kurang.append("Material kurang (butuh 20)")
        if data_pusat.sumber_daya["Obat"] < 5:
            kurang.append("Obat kurang (butuh 5)")
        if sum(1 for s in data_pusat.survivors if s.level >= 10) < 1:
            kurang.append("Butuh 1 survivor level 10")

    elif next_level == 3:
        if data_pusat.sumber_daya["Makanan"] < 30:
            kurang.append("Makanan kurang (butuh 30)")
        if data_pusat.sumber_daya["Material"] < 30:
            kurang.append("Material kurang (butuh 30)")
        if data_pusat.sumber_daya["Obat"] < 10:
            kurang.append("Obat kurang (butuh 10)")
        if sum(1 for s in data_pusat.survivors if s.level >= 20) < 1:
            kurang.append("Butuh 1 survivor level 20")

    elif next_level == 4:
        if data_pusat.sumber_daya["Makanan"] < 40:
            kurang.append("Makanan kurang (butuh 40)")
        if data_pusat.sumber_daya["Material"] < 40:
            kurang.append("Material kurang (butuh 40)")
        if data_pusat.sumber_daya["Obat"] < 20:
            kurang.append("Obat kurang (butuh 20)")
        if sum(1 for s in data_pusat.survivors if s.level >= 30) < 2:
            kurang.append("Butuh 2 survivor level 30")

    elif next_level == 5:
        if data_pusat.sumber_daya["Makanan"] < 80:
            kurang.append("Makanan kurang (butuh 80)")
        if data_pusat.sumber_daya["Material"] < 80:
            kurang.append("Material kurang (butuh 80)")
        if data_pusat.sumber_daya["Obat"] < 50:
            kurang.append("Obat kurang (butuh 50)")
        if sum(1 for s in data_pusat.survivors if s.level >= 100) < 1:
            kurang.append("Butuh 1 survivor level 100")

    if kurang:
        print("\n❌ Tidak bisa upgrade! Syarat belum terpenuhi:")
        for k in kurang:
            print("-", k)
        return False

    return True

# UPGRADE CAMP
def upgrade_camp():

    next_level = data_pusat.camp_level + 1

    print(f"\nMencoba upgrade ke Level {next_level}...")

    if not check_upgrade():
        return

    # KURANG RESOURCE
    if next_level == 2:
        data_pusat.sumber_daya["Makanan"] -= 20
        data_pusat.sumber_daya["Material"] -= 20
        data_pusat.sumber_daya["Obat"] -= 5

    elif next_level == 3:
        data_pusat.sumber_daya["Makanan"] -= 30
        data_pusat.sumber_daya["Material"] -= 30
        data_pusat.sumber_daya["Obat"] -= 10

    elif next_level == 4:
        data_pusat.sumber_daya["Makanan"] -= 40
        data_pusat.sumber_daya["Material"] -= 40
        data_pusat.sumber_daya["Obat"] -= 20

    elif next_level == 5:
        data_pusat.sumber_daya["Makanan"] -= 80
        data_pusat.sumber_daya["Material"] -= 80
        data_pusat.sumber_daya["Obat"] -= 50

    data_pusat.camp_level = next_level

    print(f"\nCamp berhasil upgrade ke Level {next_level}!")

    fitur_log.add_single_log(f"Camp di-upgrade ke Level {next_level}")

    fitur_log.add_double_log(f"Camp di-upgrade ke Level {next_level}")
    
    check_achievements()

# SISTEM PERGANTIAN HARI   
def next_day():

    # Ketika event camp rusak muncul maka next_day = block
    if data_pusat.camp_damaged:
        print("\nCamp rusak, tidak bisa mengganti hari")
        print("Perbaiki camp terlebih dahulu")
        return
        
    if data_pusat.sick_survivors:
        print("\n💀 KORBAN PENYAKIT HARI INI:")

        dead = []

        for s in data_pusat.survivors:
            if s.nama.lower() in data_pusat.sick_survivors:
                print(f"   - {s.nama} mati karena tidak segera diobati")
                dead.append(s)

        for s in dead:
            fitur_log.add_single_log(f"{s.nama} meninggal karena penyakit")

            fitur_log.add_double_log(f"{s.nama} meninggal karena penyakit")

            data_pusat.survivors.remove(s)
        
        data_pusat.total_survivor_dead += len(dead)

        if len(data_pusat.survivors) < data_pusat.min_survivor_reached:
            data_pusat.min_survivor_reached = len(data_pusat.survivors)

        data_pusat.sick_survivors.clear() 
       
    data_pusat.hari += 1

    # Reset eksplor cost
    data_pusat.explore_count = 0

    # Istirahat
    for s in data_pusat.survivors:
        if s.energi >= 0 and s.nama.lower() not in data_pusat.sick_survivors:
            rest_energy = 50

            if data_pusat.camp_level >= 2:
                rest_energy = 70

            s.energi += rest_energy
            if s.energi > 100:
                s.energi = 100

    print("\n============================================================")
    print(f"                         HARI KE {data_pusat.hari}")
    print("============================================================")

    # EVENT NORMAL
    events = [
        "Menemukan makanan tambahan",
        "Survivor sakit",
        "Camp rusak",
        "Menemukan peti logistik",
        "Tidak terjadi apa-apa"
    ]

    if data_pusat.camp_level >= 3:
        events.extend([
            "Tidak terjadi apa-apa",
            "Menemukan peti logistik",
            "Menemukan makanan tambahan"
        ])

    event = random.choice(events)

    print("\nEvent Hari Ini:", event)

    # Event makanan
    if event == "Menemukan makanan tambahan":
        data_pusat.sumber_daya["Makanan"] += 2
        print("\n+2 makanan")
            
    # Event sakit    
    elif event == "Survivor sakit" and data_pusat.survivors:
        if data_pusat.survivors:
            jumlah_sakit = random.randint(1, len(data_pusat.survivors))
            sick_list = random.sample(data_pusat.survivors, jumlah_sakit)
            print("\n💀 WABAH PENYAKIT MELANDA!")

            for sick in sick_list:
                sick.energi = 0
                data_pusat.sick_survivors[sick.nama.lower()] = True
                print(f"   - {sick.nama} jatuh sakit (energi drop ke 0)")

    # Event camp rusak
    elif event == "Camp rusak":
        data_pusat.camp_damaged = True
        print("\nCamp rusak!")
        print("Camp harus diperbaiki")

    # Event peti logistik
    elif event == "Menemukan peti logistik":
        data_pusat.sumber_daya["Makanan"] += 5
        data_pusat.sumber_daya["Material"] += 10
        data_pusat.sumber_daya["Obat"] += 2
        print("\n📦 Jackpot! Menemukan peti persediaan militer kuno.")
        print("+5 Makanan, +10 Material, +2 Obat didapatkan")

    print("\n============================================================")

    # RESET LOKASI SEMUA SURVIVOR KEMBALI KE CAMP SETIAP GANTI HARI
    for survivor in data_pusat.survivors:
        survivor.lokasi = "Camp"
    

    fitur_log.add_single_log(f"Hari {data_pusat.hari}: {event}")
    fitur_log.add_double_log(f"Hari {data_pusat.hari}: {event}")
    check_achievements()

# SAVE GAME
def save_game():

    data = {

        # DATA UTAMA
        "hari": data_pusat.hari,
        "sumber_daya": data_pusat.sumber_daya.copy(),

        "camp_level": data_pusat.camp_level,
        "camp_damaged": data_pusat.camp_damaged,

        "sick_survivors": data_pusat.sick_survivors,

        "explore_count": data_pusat.explore_count,

        # SURVIVOR
        "survivors": [
            s.to_dict() for s in data_pusat.survivors
        ],

        # EKSPLORASI
        "stack_eksplorasi": data_pusat.stack_eksplorasi.copy(),

        "queue_eksplorasi": data_pusat.queue_eksplorasi.copy(),

        "area_dikunjungi": list(data_pusat.area_dikunjungi),

        # ACHIEVEMENT
        "achievements": data_pusat.achievements,

        # HISTORY
        "total_survivor_created":
        data_pusat.total_survivor_created,

        "total_survivor_dead":
        data_pusat.total_survivor_dead,

        "max_survivor_reached":
        data_pusat.max_survivor_reached,

        "min_survivor_reached":
        data_pusat.min_survivor_reached,

        # LOG SINGLE LINKED LIST
        "single_logs": [],

        # LOG DOUBLE LINKED LIST
        "double_logs": [],

        # CURRENT TURN
        "current_turn": None
    }

    # SAVE SINGLE LINKED LIST
    current = data_pusat.log_head

    while current:
        data["single_logs"].append(current.data)
        current = current.next

    # SAVE DOUBLE LINKED LIST
    current = data_pusat.double_head

    while current:
        data["double_logs"].append(current.data)
        current = current.next

    # SAVE CURRENT TURN
    if data_pusat.current_turn:
        data["current_turn"] = (
            data_pusat.current_turn.survivor.nama
        )

    # SAVE JSON
    with open("game_data/save_data.json", "w") as file:
        json.dump(data, file, indent=4)

    print("\n💾 Game berhasil disimpan")

# LOAD GAME
def load_game():

    try:
        with open("game_data/save_data.json", "r") as file:
            data = json.load(file)

        # RESET DATA
        data_pusat.survivors.clear()

        data_pusat.log_head = None

        data_pusat.double_head = None
        data_pusat.double_tail = None

        data_pusat.circular_head = None
        data_pusat.current_turn = None

        # LOAD DATA UTAMA
        data_pusat.hari = data["hari"]

        data_pusat.sumber_daya = (
            data["sumber_daya"]
        )

        data_pusat.camp_level = (
            data["camp_level"]
        )

        data_pusat.camp_damaged = (
            data["camp_damaged"]
        )

        data_pusat.sick_survivors = (
            data["sick_survivors"]
        )

        data_pusat.explore_count = (
            data["explore_count"]
        )

        # LOAD EKSPLORASI
        data_pusat.stack_eksplorasi = (
            data["stack_eksplorasi"]
        )

        data_pusat.queue_eksplorasi = (
            data["queue_eksplorasi"]
        )

        data_pusat.area_dikunjungi = set(
            data["area_dikunjungi"]
        )

        # LOAD ACHIEVEMENT
        data_pusat.achievements = (
            data["achievements"]
        )

        # LOAD HISTORY
        data_pusat.total_survivor_created = (
            data["total_survivor_created"]
        )

        data_pusat.total_survivor_dead = (
            data["total_survivor_dead"]
        )

        data_pusat.max_survivor_reached = (
            data["max_survivor_reached"]
        )

        data_pusat.min_survivor_reached = (
            data["min_survivor_reached"]
        )

        # LOAD SURVIVOR
        for s in data["survivors"]:

            survivor = Survivor(
                s["nama"],
                s["energi"],
                s["level"],
                s["exp"],
                s["lokasi"]
            )

            data_pusat.survivors.append(
                survivor
            )

            # CIRCULAR LINKED LIST
            fitur_log.add_circular_survivor(
                survivor
            )

        # LOAD SINGLE LOG
        for log in data["single_logs"]:
            fitur_log.add_single_log(log)

        # LOAD DOUBLE LOG
        for log in data["double_logs"]:
            fitur_log.add_double_log(log)

        # LOAD CURRENT TURN
        current_name = data["current_turn"]

        if current_name and data_pusat.circular_head:

            current = data_pusat.circular_head

            while True:

                if (
                    current.survivor.nama
                    == current_name
                ):

                    data_pusat.current_turn = current
                    break

                current = current.next

                if current == data_pusat.circular_head:
                    break

        print("\n📂 Game berhasil dimuat")

    except FileNotFoundError:
        print("\n❌ Save data tidak ditemukan")

    except json.JSONDecodeError:
        print("\n❌ Save data rusak")