import pygame #підключення бібліотеки pygame
pygame.init()


back = (50, 45, 50) #створення кольору для головного вікна
mw = pygame.display.set_mode((1000, 750)) #створення головного вікна
mw.fill(back) #заповнення головного вікна
clock = pygame.time.Clock() #створення таймера
bd_image = pygame.image.load('fonn.png')


class Area(): #клас для створення меж об'єкту
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)      
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
class Label(Area): #клас для створення надписів
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Area): #клас для прикріплення зображень
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Wall(Area):
    def __init__(self,x=0,y=0,width=0,height=0,color=(22,26,31)):
        super().__init__(x,y,width,height,color)

walls = [Wall(0,550,1000,300),
         Wall(150,450,50,150),
         Wall(300,350,50,250),
         Wall(450,250,100,350),
         Wall(650,350,50,250),
         Wall(800,450,50,150)]








class Player(Picture):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(filename,x,y,width,height)
        self.gravity = 0.5 #гравітація (швидкість падіння вниз)
        self.jump_power = -11 #величина стрибка
        self.vel_y = 0 #швидкість руху в стрибку

    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                elif self.vel_y < 0:
                    self.rect.top = w.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            self.can_jump = False

player = Player('ball.png',100,200,50,50) #створення об'єкту



move_left = False
move_right = False

game = True
while game: #створення головного циклу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN: # якщо натиснута клавіша
            if event.key == pygame.K_d: # якщо клавіша "праворуч"
                move_right = True
            if event.key == pygame.K_a: # якщо клавіша "ліворуч"
                move_left = True

            if event.key == pygame.K_w:

                player.jump()

        elif event.type == pygame.KEYUP: # якщо клавіша відпущена
            if event.key == pygame.K_d: # якщо клавіша "праворуч"
                move_right = False
            if event.key == pygame.K_a: # якщо клавіша "ліворуч"
                move_left = False

    text1 = Label(20,20,20,10,(0,0,0)) # перші 2 цифри це координати
    text1.set_text('Text',60,(255,0,0)) # 60 - це розмір тексту, і далі 2 цифри це колір
    text1.draw(20,20)

    player.move()

    if move_right:
        player.rect.x += 3
    if move_left:
        player.rect.x -= 3

    if move_right:
        player.rect.x += 3
        for w in walls:
            if player.rect.colliderect(w.rect):
                player.rect.right = w.rect.left  # змінюємо позицію гравця, щоб він не міг пройти крізь стіну
    if move_left:
        player.rect.x -= 3
        for w in walls:
            if player.rect.colliderect(w.rect):
                player.rect.left = w.rect.right  # змінюємо позицію гравця, щоб він не міг пройти крізь стіну

    


    mw.blit(bd_image, (0,0)) #заповнення головного вікна


    player.fill()
    player.draw()
    



    for w in walls:
        w.fill()
 
    pygame.display.update() #оновлення кадрів
    clock.tick(60) # фпс