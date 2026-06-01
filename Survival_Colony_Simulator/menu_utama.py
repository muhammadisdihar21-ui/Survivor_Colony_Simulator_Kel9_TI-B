from game_data import data_pusat
from features import fitur_survivor
from features import fitur_eksplorasi
from features import fitur_log
from features import fitur_camp
from features import fitur_achievement
from features import fitur_tutorial
from colorama import Fore, Style #type: ignore
import os

def header():
        print("\n" + "="*60)
        print("                 SURVIVAL COLONY SIMULATOR")
        print("="*60)
        print(f"Hari           : {data_pusat.hari}")
        print(f"Camp Level     : {data_pusat.camp_level}")
        if data_pusat.camp_damaged:
            print(f"Status Camp    : {Fore.RED}Rusak{Style.RESET_ALL}")
        else:
            print(f"Status Camp    : {Fore.GREEN}Aman{Style.RESET_ALL}")
        jumlah_sakit = len(data_pusat.sick_survivors)
        if jumlah_sakit > 0:
            print(f"Survivor Sakit : {Fore.RED}{jumlah_sakit}{Style.RESET_ALL}")
        else:
            print(f"Survivor Sakit : {jumlah_sakit}")
        print("="*60)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_survivor():
    while True:
        clear_screen()
        header()
        print("\n👥 SURVIVOR")
        print("-"*60)
        print("[1] ➕ Tambah Survivor")
        print("[2] 👥 Tampilkan Survivor")
        print("[3] 🔍 Cari Survivor")
        print("[4] 📊 Urutkan Survivor")
        print("[5] 🗑️  Hapus Survivor")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_survivor.add_survivor()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_survivor.view_survivors()
            input("\nENTER untuk kembali...")
        elif c == "3":
            fitur_survivor.search_survivor()
            input("\nENTER untuk kembali...")
        elif c == "4":
            fitur_survivor.sort_survivors()
            input("\nENTER untuk kembali...")
        elif c == "5":
            fitur_survivor.delete_survivor()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("\nENTER...")

def menu_resource():
    while True:
        clear_screen()
        header()
        print("\n📦 RESOURCE")
        print("-"*60)
        print("[1] 📦 Lihat Resource")
        print("[2] 🍖 Beri Makan Survivor")
        print("[3] 💊 Sembuhkan Survivor")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_camp.show_resources()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_camp.eat_food()
            input("\nENTER untuk kembali...")
        elif c == "3":
            fitur_camp.heal_survivor()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("\nENTER...")

def menu_camp():
    while True:
        clear_screen()
        header()
        print("\n🏕️  CAMP")
        print("-"*60)
        print("[1] 📖 Info Upgrade Camp")
        print("[2] ⬆️  Upgrade Camp")
        print("[3] 🔨 Perbaiki Camp")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_camp.show_upgrade_info()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_camp.upgrade_camp()
            input("\nENTER untuk kembali...")
        elif c == "3":
            fitur_camp.repair_camp()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")
    
def menu_eksplorasi():
    while True:
        clear_screen()
        header()
        print("\n🌍 EKSPLORASI")
        print("-"*60)
        print("[1] 🌍 Eksplorasi Area")
        print("[2] 📜 Antrean Eksplorasi")
        print("[3] ↩️  Backtrack Area")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_eksplorasi.explore_area()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_eksplorasi.process_queue()
            input("\nENTER untuk kembali...")
        elif c == "3":
            fitur_eksplorasi.backtrack_area()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")

def menu_log():
    while True:
        clear_screen()
        header()
        print("\n🧠 LOG / DATA")
        print("-"*60)
        print("[1] 📜 Riwayat Aktivitas")
        print("[2] ➡️  Riwayat Maju")
        print("[3] ⬅️  Riwayat Mundur")
        print("[4] 🔄 Rotasi Survivor")
        print("[5] 🎯 Giliran Survivor")
        print("[6] 🌍 Status Area Eksplorasi")
        print("[7] 🗺️  Peta Struktur Area")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_log.show_single_log()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_log.show_double_forward()
            input("\nENTER untuk kembali...")
        elif c == "3":
            fitur_log.show_double_backward()
            input("\nENTER untuk kembali...")
        elif c == "4":
            fitur_log.show_circular_survivor()
            input("\nENTER untuk kembali...")
        elif c == "5":
            fitur_log.next_turn()
            input("\nENTER untuk kembali...")
        elif c == "6":
            fitur_eksplorasi.recursive_area()
            input("\nENTER untuk kembali...")
        elif c == "7":
            fitur_eksplorasi.show_tree(data_pusat.area_tree)
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")

def menu_save():
    while True:
        clear_screen()
        header()
        print("\n💾 SAVE / LOAD")
        print("-"*60)
        print("[1] 💾 Save Game")
        print("[2] 📂 Load Game")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_camp.save_game()
            input("\nENTER untuk kembali...")
        elif c == "2":
            fitur_camp.load_game()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")


def menu_achievement():
    while True:
        clear_screen()
        header()
        print("\n🏆 ACHIEVEMENT")
        print("-"*60)
        print("[1] 🏅 Achievement")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")
        if c == "1":
            if data_pusat.camp_level < 5:
                print("\n🔒 Unlock camp level 5 dulu")
                input("\nENTER untuk kembali...")
            else:
                fitur_achievement.show_achievements()
                input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")

def menu_nextday():
    while True:
        clear_screen()
        header()
        print("\n⏳ EVENT / WAKTU")
        print("-"*60)
        print("[1] 🌄 Hari Berikutnya")
        print("[0] 🔙 Kembali")
        print("-"*60)

        c = input("Pilih: ")

        if c == "1":
            fitur_camp.next_day()
            input("\nENTER untuk kembali...")
        elif c == "0":
            break
        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")

# SURVIVAL COLONY SIMULATOR
# MAIN PROGRAM
def main():
    while True:
        clear_screen()
        header()

        print("\n📌 MENU UTAMA")
        print("-"*60)
        print("[0] 📖 Tutorial Game")
        print("[1] 👥 Survivor")
        print("[2] 📦 Resource")
        print("[3] 🏕️  Camp")
        print()
        print("[4] 🌍 Eksplorasi")
        print("[5] ⏳ Event / Waktu")
        print("[6] 🧠 Log / Data")
        print()
        print("[7] 💾 Save / Load")
        print("[8] 🏆 Achievement")
        print("[9] 🚪 Exit")
        print("-"*60)
        

        choice = input("\nPilih menu: ")

        if choice == "1":
            menu_survivor()

        elif choice == "2":
            menu_resource()

        elif choice == "3":
            menu_camp()

        elif choice == "4":
            menu_eksplorasi()

        elif choice == "5":
            menu_nextday()

        elif choice == "6":
            menu_log()

        elif choice == "7":
            menu_save()

        elif choice == "8":
            menu_achievement()
        
        elif choice == "0":
            clear_screen()
            header()
            fitur_tutorial.show_tutorial()
            input("\nENTER untuk kembali...")

        elif choice == "9":
            print("\n👋 Program selesai\n")
            break

        else:
            print("\n❌ Menu tidak valid")
            input("ENTER...")

# Menjalankan program
if __name__ == "__main__":
    main()
