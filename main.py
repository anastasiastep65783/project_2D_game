import pygame

# размер окна игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# загрузка фона для игры
fon = pygame.image.load('fon.png')

# класс действий игрока
class Player(pygame.sprite.Sprite):
    # игрок смотрит вправо
    right = True

    def __init__(self):
        super().__init__()

        # изображение игрока
        self.image = pygame.image.load('igrok.png')

        # границы персонажа
        self.rect = self.image.get_rect()

        # скорость игрока
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # гравитация
        self.calc_grav()

        # передвижение вправо-влево
        self.rect.x += self.change_x

        # слежка за столкновением с объектами
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # перебор объектов
        for block in block_hit_list:
            # если движение вправо, установление правой стороны игрока
            # на левую сторону объекта, с которым произошло столкновение
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # ситуация наоборот
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # движение вверх вниз
        self.rect.y += self.change_y

        # ситуация как с право-лево, но вверх-вниз
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # остановка движения вправо-влево
            self.change_y = 0

    def calc_grav(self):
        # скорость падения объекта
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

        # если на земле, то позиция y как 0
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # обработка прыжка
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        # прыжок вверх, если всё в порядке
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -16

    # передвижение влево
    def go_left(self):
        self.change_x = -9
        if (self.right):
            self.flip()
            self.right = False

    # передвижение вправо
    def go_right(self):
        self.change_x = 9
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        # стоять, если не задействуются клавиши
        self.change_x = 0

    def flip(self):
        # игрок переворачивается
        self.image = pygame.transform.flip(self.image, True, False)


