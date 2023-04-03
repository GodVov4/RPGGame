import random


class Bcolors:
    HEADER = "\33[95m"
    OKBLUE = "\33[94m"
    OKGREEN = "\33[92m"
    WARNING = "\33[93m"
    FAIL = "\33[91m"
    ENDC = "\33[0m"
    BOLD = "\33[1m"
    UNDERLINE = "\33[4m"


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Атака", "Магія", "Речі"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(f"\n{Bcolors.BOLD}    {self.name}{Bcolors.ENDC}")
        print(f"{Bcolors.OKBLUE}{Bcolors.BOLD}    ДІЯ:{Bcolors.ENDC}")
        for item in self.actions:
            print(f"        {str(i)}.{item}")
            i += 1

    def choose_magic(self):
        i = 1
        print(f"\n{Bcolors.OKBLUE}{Bcolors.BOLD}    МАГІЯ:{Bcolors.ENDC}")
        for spell in self.magic:
            print(f"        {str(i)}.{spell.name} (ціна:{str(spell.cost)})")
            i += 1

    def choose_item(self):
        i = 1
        print(f"\n{Bcolors.OKBLUE}{Bcolors.BOLD}    РЕЧІ:{Bcolors.ENDC}")
        for item in self.items:
            print(f"        {str(i)}.{item.name} : {item.discription} (x{item.quantity})")
            i += 1

    @staticmethod
    def choose_target(enemies):
        i = 1
        print(f"\n{Bcolors.FAIL}{Bcolors.BOLD}    ЦІЛЬ:{Bcolors.ENDC}")
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print(f"        {str(i)}.{enemy.name}")
                i += 1
        choice = int(input("Вибрати ціль: ")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 50

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        len_hp_spaces = len(str(self.maxhp)) - len(str(self.hp))
        hp_spaces = ""
        hp_spaces += " " * len_hp_spaces

        print("                      __________________________________________________")
        print(f"{Bcolors.BOLD}{self.name}:    {hp_spaces}{self.hp}/{self.maxhp}"
              f"│{Bcolors.FAIL}{hp_bar}{Bcolors.ENDC}│")
        print("                      ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    def get_stats(self):
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 25
        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        len_hp_spaces = len(str(self.maxhp)) - len(str(self.hp))
        hp_spaces = ""
        hp_spaces += " " * len_hp_spaces
        len_mp_spaces = len(str(self.maxmp)) - len(str(self.mp))
        mp_spaces = ""
        mp_spaces += " " * len_mp_spaces

        print("                   _________________________           __________")
        print(f"{Bcolors.BOLD}{self.name}:    {hp_spaces}{self.hp}/{self.maxhp}"
              f"│{Bcolors.OKGREEN}{hp_bar}{Bcolors.ENDC}│    "
              f"{Bcolors.BOLD}{mp_spaces}{self.mp}/{self.maxmp}│{Bcolors.OKBLUE}{mp_bar}{Bcolors.ENDC}│")
        print("                   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯           ¯¯¯¯¯¯¯¯¯¯")

    def choose_enemy_spell(self):
        magic_choise = random.randrange(len(self.magic))
        spell = self.magic[magic_choise]
        magic_dmg = spell.generate_damage()
        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
