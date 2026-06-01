from models.komponen_game import Area

# LIST
# Menyimpan data survivor
survivors = []

# HASH TABLE / DICTIONARY
# Menyimpan data resource
sumber_daya = {
    "Makanan": 0,
    "Material": 0,
    "Obat": 0
}

# Simulasi hari
hari = 1

# STACK
# Menyimpan history eksplorasi
stack_eksplorasi = []

# QUEUE
# Menyimpan antrean eksplorasi
queue_eksplorasi = []

# SET
# Menyimpan area yang sudah dikunjungi
area_dikunjungi = set()

# GRAPH
# Hubungan antar area
area_graph = {
    "Camp": ["Hutan", "Sungai"],
    "Hutan": ["Kota Terbengkalai", "Sungai"],
    "Sungai": ["Gua", "Hutan"],
    "Kota Terbengkalai": ["Hutan"],
    "Gua": ["Sungai"]
}

# TREE
# Struktur area eksplorasi
area_tree = {
    "Camp": {
        "Hutan": {
            "Kota Terbengkalai": {}
        },
        "Sungai": {
            "Gua": {}
        }
    }
}

# TUPLE
# Koordinat area
data_area = {
    "Hutan": Area("Hutan", ["Material", "Makanan"], (1, 2)),
    "Sungai": Area("Sungai", ["Makanan"], (3, 4)),
    "Kota Terbengkalai": Area("Kota Terbengkalai", ["Obat", "Makanan"], (5, 1)),
    "Gua": Area("Gua", ["Material", "Obat"], (6, 2))
}

# SINGLE LINKED LIST
log_head = None

# DOUBLE LINKED LIST
double_head = None
double_tail = None

# CIRCULAR LINKED LIST
circular_head = None
current_turn = None

# SISTEM BARU
explore_count = 0
camp_damaged = False
sick_survivors = {}
        
# LEVEL CAMP
camp_level = 1

# BIAYA UPGRADE CAMP
camp_upgrade_cost = {
    2: {"Makanan": 20, "Material": 20, "Obat": 5},
    3: {"Makanan": 30, "Material": 30, "Obat": 10},
    4: {"Makanan": 40, "Material": 40, "Obat": 20},
    5: {"Makanan": 80, "Material": 80, "Obat": 50}
}

# ACHIEVEMENT SYSTEM
# ===== ACHIEVEMENT TRACKING =====
achievements = []

# ===== HISTORY TRACKING =====
total_survivor_created = 0
total_survivor_dead = 0

max_survivor_reached = 1
min_survivor_reached = 999