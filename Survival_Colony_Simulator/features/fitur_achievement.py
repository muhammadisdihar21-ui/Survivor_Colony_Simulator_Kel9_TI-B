from game_data import data_pusat

def check_achievements():
    s = data_pusat.survivors
    day = data_pusat.hari
    camp = data_pusat.camp_level

    max_s = data_pusat.max_survivor_reached
    min_s = data_pusat.min_survivor_reached
    created = data_pusat.total_survivor_created
    dead = data_pusat.total_survivor_dead

    # ===== DAY =====
    if day >= 7:
        add_achievement("Awal Bertahan", "Bertahan 7 hari")
    if day >= 30:
        add_achievement("Survivor Tangguh", "Bertahan 30 hari")
    if day >= 100:
        add_achievement("Legenda", "Bertahan 100 hari")

    # ===== SURVIVOR HISTORY =====
    if max_s >= 3:
        add_achievement("Koloni Terbentuk", "Pernah punya 3 survivor")
    if max_s >= 10:
        add_achievement("Koloni Besar", "Pernah mencapai 10 survivor")
    if min_s <= 2 and max_s >= 5:
        add_achievement("Koloni Hancur", "Pernah besar lalu menyusut")

    # ===== LEVEL =====
    if any(x.level >= 10 for x in s):
        add_achievement("Survivor Terlatih", "Ada survivor level 10+")
    if any(x.level >= 50 for x in s):
        add_achievement("Veteran", "Ada survivor level 50+")
    if any(x.level >= 100 for x in s):
        add_achievement("Legenda Hidup", "Ada survivor level 100+")

    # ===== CAMP =====
    if camp >= 2:
        add_achievement("Camp Bertahan", "Camp level 2")
    if camp >= 3:
        add_achievement("Camp Kuat", "Camp level 3")
    if camp >= 5:
        add_achievement("Peradaban Baru", "Camp level 5")

    # ===== DEATH =====
    if dead >= 1:
        add_achievement("Korban Pertama", "Ada survivor mati")
    if dead >= 5:
        add_achievement("Koloni Berdarah", "Banyak kematian")
    if dead == 0 and day >= 50:
        add_achievement("Perfect Colony", "50 hari tanpa kematian")

    # ===== CREATED =====
    if created >= 5:
        add_achievement("Recruiter Awal", "Pernah merekrut 5 survivor")

    if created >= 15:
        add_achievement("Koloni Berkembang", "Pernah merekrut 15 survivor")

    # ===== COMBO =====
    if created >= 10 and dead >= 5:
        add_achievement("Koloni Penuh Perjuangan", "Banyak rekrut dan banyak kehilangan")

    if created >= 10 and len(s) <= 3:
        add_achievement("Sisa Harapan", "Pernah besar tapi hanya sedikit bertahan")

    if len(s) <= 3 and day >= 50:
        add_achievement("Last Standing", "Sedikit survivor bertahan lama")

    if any(x.level >= 50 for x in s) and len(s) <= 3:
        add_achievement("Elite Solo", "Kuat walau sedikit")

    if day <= 20 and any(x.level >= 50 for x in s):
        add_achievement("Fast Evolution", "Cepat naik level")

    if max_s >= 5 and len(s) <= 3:
        add_achievement("Fall of Colony", "Koloni pernah besar lalu runtuh")

    if any(x.level >= 30 for x in s) and len(s) >= 5 and day >= 30:
        add_achievement("Balanced Colony", "Koloni kuat dan stabil")

def add_achievement(name, desc):
    for a in data_pusat.achievements:
        if a["name"] == name:
            return

    data_pusat.achievements.append({
        "name": name,
        "desc": desc
    })

def show_achievements():
    print("\n" + "="*60)
    print("                   🏆 ACHIEVEMENT COLONY")
    print("="*60)

    if not data_pusat.achievements:
        print("\n🔒 Belum ada achievement yang terbuka")
        print("="*60)
        return

    print(f"\nTotal Unlocked: {len(data_pusat.achievements)}\n")
    print("-"*60)
    for i, ach in enumerate(data_pusat.achievements, 1):
        print(f"🏆 {i}. {ach['name']}")
        print(f"      📌 {ach['desc']}")
        print("-"*60)
        
    print()
    print("="*60)