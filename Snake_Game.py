import os, time
import msvcrt
from random import randint
UP, DOWN, LEFT, RIGHT = 72, 80, 75, 77 # Ce sont les codes ASCII pour les bouttons des flèches du clavier

class Cadre:
    def __init__(self, longueur, largeur):
        self.longueur = longueur
        self.largeur = largeur

class Snake:
    isAlive = True
    def __init__(self, length, coords, direction):
        self.length = length
        self.coords = coords
        self.direction = direction
    
    def manger(self):
        self.length += 1 # Incrementer taille de Snake
    
    def bouger(self):
        head = self.coords[0] # Référence à la tete de notre snake
         # Ajouter un point à chaque mouvement en fonction de la direction
        if self.direction == UP:
            self.coords.insert(0, (head[0], head[1]-1)) # Ajouter un point en haut de la tête
        elif self.direction == RIGHT:
            self.coords.insert(0, (head[0]+1, head[1])) # Ajouter un point à droite de la tête
        elif self.direction == DOWN:
            self.coords.insert(0, (head[0], head[1]+1))  # Ajouter un point en bas de la tête
        elif self.direction == LEFT:
            self.coords.insert(0, (head[0]-1, head[1]))  # Ajouter un point à gauche de la tête

        if(len(self.coords) > self.length): # Si le nombre de points occupés dépasse la taille de snake
            self.coords.pop() # supprimer le dernier point

class Nourriture:
    def __init__(self, position):
        self.position = position # initialiser la position

    def regenerer(self, max_x, max_y):  # max_x et max_y sont là pour que la nourriture ne soit pas regenerée en dehors des bourdures du cadre
        self.position = (randint(0, max_x), randint(0, max_y)) # choisir une position aléatoire entre 0 et la bordure

class Game:
    frame = 1 # compteur de nombre de cadres dessinés (à chaque fois que l'écran s'efface et se redessine/ le nombre de fois où le terminal s'efface)
    highscore = 0 # compteur de record
    score = 0 # compteur de score
    def clearScreen(self):
        os.system("cls")

    def mainMenu(self):
        if os.path.exists("score.txt"):
            f = open("score.txt", "r")  #  Ouvrir le fichier de score (en mode lecture)
            self.highscore = int(f.read()) # Lire le plus haut score enregistré
            f.close()   # Pour fermer le fichier aprés la lecture
        
        record = f"Record: {self.highscore} "   # Pour afficher le Record dans le menu 
        record_line = " " * (60 - len(record)) + record     # Pour que la ligne ne sorte pas du cadre
        
        while True:
            self.clearScreen()
            # Main Menu
            print("╔════════════════════════════════════════════════════════════╗")
            print("║"                     + record_line +                      "║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                 Welcome to my Snake game!                  ║")
            print("║                    N - Nouvelle partie                     ║")
            print("║                      Q - Quitter jeu                       ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                                            ║")
            print("║                                             DAHMANI Alicia ║")
            print("╚════════════════════════════════════════════════════════════╝")
            answer = input("Votre choix: ") #Pour que le joueur fasse un choix

            if(answer.lower() == "n"):  # On a utilisé la fonction "lower()" pour que peu importe si le joueur l'écrit en majuscule ou miniscule, la réponse sera acceptée
                break   # Pour sortir de la boucle et 

            elif(answer.lower() == "q"):
                print("Au revoir ! Et merci d'avoir joué à Snake")
                exit()

    def run(self):
        # Initialiser les objets de notre jeu
        cadre = Cadre(longueur=60, largeur=16) # Cadre (terrain de jeu)
        snake = Snake(length=3, coords=[(3,10), (2,10), (1,10)], direction=RIGHT) # Snake (notre joeur)
        nourriture = Nourriture(position= (5, 10)) # Nourriture, initialisé à un point fixe au départ

        # Boucle infini pour progresser dans le jeu
        while True:
            # Effacer l'écran
            self.clearScreen()

            # Lecture d'input
            if msvcrt.kbhit():  #on utilise la bibliothèque de python "MS VC++ runtime"  et la fonction "keyboard hit"
                direction = msvcrt.getch()  # Pour lire les flèches
                while msvcrt.kbhit():
                    direction = msvcrt.getch()
                
                direction = ord(direction)  # lire le code ASCII de la touche appuyée
               
                if (direction == UP and snake.direction != DOWN):     # pour éviter qu'il aille en haut directement alors qu'il se dérigeait vers le bas
                    snake.direction = UP
                elif (direction == RIGHT and snake.direction != LEFT):
                    snake.direction = RIGHT
                elif (direction == DOWN and snake.direction != UP):
                    snake.direction = DOWN
                elif (direction == LEFT and snake.direction != RIGHT):
                    snake.direction = LEFT
            
            # Mouvement de snake
            if (snake.isAlive): # Si le snake est en vie
                snake.bouger() # Avancer notre snake d'un pas

            # Logique de manger
            if snake.coords[0] == nourriture.position:
                snake.manger()
                nourriture.regenerer(max_x=cadre.longueur-1, max_y=cadre.largeur-1) # Pour regenerer la nourriture aprés l'avoir mangé à un autre endroit
                self.score += 1 # Pour augmenter le score à chaque fois que le snake mange
                
            # Logique de collision (avec le mur et avec soi)
            head = snake.coords[0]
            if head[0] == 0 or head[0] == cadre.longueur or head[1] == 0 or head[1] == cadre.largeur:   # La collision avec le cadre
                snake.isAlive = False
            if (head in snake.coords[1:]): # Pour la collision avec son corps
                snake.isAlive = False
                
            # Affichage de frames et du score
            frame_counter = f"Frame: {self.frame}"
            score_counter = f"Score: {self.score}"
            spaces = " " * (cadre.longueur - (len(frame_counter) + len(score_counter)) + 1)
            print(frame_counter + spaces + score_counter)
            self.frame = self.frame+1

            # Affichage du cadre, Snake et de la nourriture
            print("╔"+ ("═" * cadre.longueur) +"╗")
            for ligne in range(cadre.largeur):
                print("║", end="")
                for colonne in range(cadre.longueur):
                    if (colonne, ligne) in snake.coords:
                        print("O", end="")
                    elif (colonne, ligne) == nourriture.position:
                        print("*", end="")
                    else:
                        print(" ", end="")
                print("║")
            print("╚" + ("═" * cadre.longueur) +"╝")
            
            if not snake.isAlive:  # En cas de mort du snake = la condition isAlive n'est plus valide
                print(f"Game Over :( Votre score est de {self.score}!") # Pour afficher le score en utilisant format
                if(self.score > self.highscore):    # Si on a eu un score plus elevé ==> on l'enrergistre dans le fichier
                    f = open("score.txt", "w")
                    f.write(str(self.score))
                    f.close()
                break

            # Sleep 0.2s = le temps pour effacer le terminal et l'afficher à nouveau
            time.sleep(0.2)

if __name__ == "__main__" :
    myGame = Game() # Créer une instance de jeu
    myGame.mainMenu() # Lancer le main menu
    myGame.run() # Lancer le jeu
