import random

class Case:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return f"({self.x}, {self.y})"

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def adjacentes(self, jeu):
    adj = []
    for dx in [-1, 0, 1]:
      for dy in [-1, 0, 1]:
        if dx != 0 or dy != 0:  # Exclude (0, 0) for no movement
          new_x = self.x + dx
          new_y = self.y + dy
          if 0 <= new_x < jeu.taille and 0 <= new_y < jeu.taille:
            adj.append(jeu.plateau[new_x][new_y])
    return adj

class Creature:
  def __init__(self, nom, position):
    self.nom = nom
    self.position = position

  def __str__(self):
    return f"{self.nom} - Position: {self.position}"

  def choisirCible(self, jeu):
    adj_cases = self.position.adjacentes(jeu)
    cases_occupees = [case for case in adj_cases if jeu.estOccupee(case)]
    if cases_occupees:
      return random.choice(cases_occupees)  # Prioritize capturing opponent
    else:
      return random.choice(adj_cases)

class Jeu:
  def __init__(self, taille):
    self.taille = taille
    self.plateau = [[Case(x, y) for y in range(taille)] for x in range(taille)]
    self.listeDesCreatures = []
    self.tour = 0
    self.actif = None

  def __str__(self):
    representation = ""
    for y in range(len(self.plateau[0])):
      for x in range(len(self.plateau)):
        case = self.plateau[y][x]
        for creature in self.listeDesCreatures:
          if creature.position == case:
            representation += f"{creature.nom[0]} "
            break
        else:
          representation += ". "
      representation += "\n"
    return representation

  def estOccupee(self, case):
    for creature in self.listeDesCreatures:
      if creature.position == case:
        return True
    return False

  def deplacer(self, creature, case):
    if case in creature.position.adjacentes(self):
      if self.estOccupee(case):
        for adversaire in self.listeDesCreatures:
          if adversaire.position == case:
            print(f"{creature.nom} a capturé {adversaire.nom} !")
            self.listeDesCreatures.remove(adversaire)
            if len(self.listeDesCreatures) == 1:
              print(f"{creature.nom} a gagné !")
              return
      creature.position = case
      self.tour += 1
      self.actif = self.listeDesCreatures[(self.tour) % len(self.listeDesCreatures)]

# Initialisation du jeu
jeu = Jeu(4)
creature1 = Creature("Creature 1", jeu.plateau[0][0])
creature2 = Creature("Creature 2", jeu.plateau[3][3])
jeu.listeDesCreatures = [creature1, creature2]
jeu.actif = creature1

# Déroulement du jeu
while len(jeu.listeDesCreatures) > 1:
  print(jeu)
  print(creature1)
  print(creature2)
  cible = creature1.choisirCible(jeu)
  jeu.deplacer(creature1, cible)
  if len(jeu.listeDesCreatures) == 1:
    break
  print(jeu)
  print(creature1)
  print(creature2)
  cible = creature2.choisirCible(jeu)
  jeu.deplacer(creature2, cible)
