import random
from classes.game import Person, Bcolors
from classes.inventory import Item
from classes.magic import Spell


# Black magic
fire = Spell("Вогонь", 10, 100, "black")
thunder = Spell("Грім", 10, 100, "black")
blizzard = Spell("Хуртовина", 10, 100, "black")
meteor = Spell("Метеорит", 20, 2000, "black")
quake = Spell("Землетрус", 14, 140, "black")


# White magic
cure = Spell("Ліки", 12, 120, "white")
cura = Spell("Подвійні ліки", 18, 180, "white")


# Items
potion = Item("Зілля", "potion", "Лікує 50 HP", 50, 15)
hipotion = Item("Подвійне Зілля", "potion", "Лікує 100 HP", 100, 2)
superpotion = Item("Супер Зілля", "potion", "Лікує 500 HP", 500, 5)
elixer = Item("Еліксир", "elixer", "Повністю відновлює HP/MP одному бійцю", 9999, 5)
hielixer = Item("Мега Еліксир", "elixer", "Повністю відновлює HP/MP союзникам", 9999, 2)
granade = Item("Граната", "attack", "Завдає 500 шкоди", 500, 5)

# Players & Enemies
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [potion, hipotion, superpotion, elixer, hielixer, granade]

player1 = Person("Володя", 450, 90, 50, 50, player_spells, player_items)
player2 = Person("Роксік", 400, 80, 80, 20, player_spells, player_items)
player3 = Person("Стьопа", 600, 50, 40, 80, player_spells, player_items)
enemy1 = Person("Абонент", 1200, 65, 45, 25, enemy_spells, [])
enemy2 = Person("Алкашик", 1200, 65, 45, 25, enemy_spells, [])
enemy3 = Person("Циганча", 1200, 65, 45, 25, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
print(f"{Bcolors.FAIL}{Bcolors.BOLD}ВОРОГ АТАКУЄ!{Bcolors.ENDC}")

while running:
    print(f"{Bcolors.WARNING}{Bcolors.BOLD}={Bcolors.ENDC}" * 20 + "\n")
    print(f"{Bcolors.BOLD}Імʼя:      HP:                                   MP:{Bcolors.ENDC}")

    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = int(input(f"{Bcolors.OKBLUE}{Bcolors.BOLD}    Вибрати дію: {Bcolors.ENDC}")) - 1

        if choice == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(f"Ти атакуєш {Bcolors.FAIL}{enemies[enemy].name}{Bcolors.ENDC} на "
                  f"{Bcolors.FAIL}{dmg}{Bcolors.ENDC} одиниць шкоди.")

            if enemies[enemy].get_hp() == 0:
                print(f"{Bcolors.FAIL}{enemies[enemy].name}{Bcolors.ENDC} помер.")
                del enemies[enemy]

        elif choice == 1:
            player.choose_magic()
            magic_choice = int(input(f"{Bcolors.OKBLUE}{Bcolors.BOLD}    Вибрати магію: {Bcolors.ENDC}")) - 1

            if magic_choice == -1:
                continue
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()
            player.reduce_mp(spell.cost)

            if spell.cost > current_mp:
                print(f"{Bcolors.FAIL}{Bcolors.BOLD}\nНЕ ВИСТАЧАЄ MP!\n{Bcolors.ENDC}")
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(f"{Bcolors.OKGREEN}\n{spell.name}{Bcolors.ENDC} зцілюють на "
                      f"{Bcolors.OKGREEN}{magic_dmg} HP.{Bcolors.ENDC}")
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(f"{Bcolors.FAIL}\n{spell.name}{Bcolors.ENDC} завдає {Bcolors.FAIL}{magic_dmg}{Bcolors.ENDC}"
                      f" одиниць шкоди для {enemies[enemy].name}.")

                if enemies[enemy].get_hp() == 0:
                    print(f"{Bcolors.FAIL}{enemies[enemy].name}{Bcolors.ENDC} помер.")
                    del enemies[enemy]

        elif choice == 2:
            player.choose_item()
            item_choice = int(input(f"{Bcolors.OKBLUE}{Bcolors.BOLD}    Вибрати річ: {Bcolors.ENDC}")) - 1

            if item_choice == -1:
                continue

            item = player_items[item_choice]

            if item.quantity == 0:
                print(f"{Bcolors.FAIL}\nНемає...{Bcolors.ENDC}")
                continue

            item.quantity -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(f"{Bcolors.OKGREEN}\n{item.name}{Bcolors.ENDC} зцілює на"
                      f" {Bcolors.OKGREEN}{str(item.prop)}{Bcolors.ENDC} HP.")
            elif item.type == "elixer":
                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(f"{Bcolors.OKGREEN}\n{item.name}{Bcolors.ENDC} повністю відновив HP/MP.")
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(f"{Bcolors.FAIL}\n{item.name}{Bcolors.ENDC} завдає"
                      f" {Bcolors.FAIL}{str(item.prop)}{Bcolors.ENDC} одиниць шкоди для"
                      f" {Bcolors.FAIL}{enemies[enemy].name}{Bcolors.ENDC}.")

                if enemies[enemy].get_hp() == 0:
                    print(f"{Bcolors.FAIL}{enemies[enemy].name}{Bcolors.ENDC} помер.")
                    del enemies[enemy]
    # Check if batle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 3:
        print(f"{Bcolors.OKGREEN}{Bcolors.BOLD}ПЕРЕМОГА!{Bcolors.ENDC}")
        running = False

    elif defeated_players == 3:
        print(f"{Bcolors.FAIL}{Bcolors.BOLD}ПРОГРАШ!{Bcolors.ENDC}")
        running = False
    # Enemy attack
    for enemy in enemies:
        enemy_choice = random.randrange(3)

        if enemy_choice == 0:
            target = random.randrange(3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(f"{Bcolors.FAIL}{enemy.name}{Bcolors.ENDC} атакує {Bcolors.OKGREEN}{players[target].name}{Bcolors.ENDC}"
                  f" на {Bcolors.FAIL}{enemy_dmg}{Bcolors.ENDC} одиниць шкоди.")

        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(f"{Bcolors.OKGREEN}\n{spell.name}{Bcolors.ENDC} зцілює {enemy.name} на "
                      f"{Bcolors.OKGREEN}{magic_dmg} HP.{Bcolors.ENDC}")
            elif spell.type == "black":
                target = random.randrange(3)
                players[target].take_damage(magic_dmg)
                print(f"{Bcolors.FAIL}\n{enemy.name} використовує {spell.name}{Bcolors.ENDC} і завдає "
                      f"{Bcolors.FAIL}{magic_dmg}{Bcolors.ENDC} одиниць шкоди для {players[target].name}.")

                if players[target].get_hp() == 0:
                    print(f"{Bcolors.FAIL}{players[target].name}{Bcolors.ENDC} помер.")
                    del players[target]
            print(f"Ворог атакує {spell} на {magic_dmg} шкоди.")
