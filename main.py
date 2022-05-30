import pygame

# размер окна игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# загрузка фона для игры
fon = pygame.image.load('fon.jpg')
start = pygame.image.load('start.jpg')
exit = pygame.image.load('exit.jpg')


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False


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


# класс описания платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        # Конструктор платформ
        super().__init__()
        # загрузка изображения платформы
        self.image = pygame.image.load('platf.png')

        # границы платформы
        self.rect = self.image.get_rect()


# класс расположения платформ
class Level(object):
    def __init__(self, player):
        # группа спрайтов
        self.platform_list = pygame.sprite.Group()
        # ссылка на основного игрока
        self.player = player

    # обновление экрана
    def update(self):
        self.platform_list.update()

    # рисование объектов
    def draw(self, screen):
        # рисование фона
        screen.blit(fon, (0, 0))

        # рисование платформ из группы спрайтов
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self, player):
        # родительский конструктор
        Level.__init__(self, player)

        # массив с данными про платформы
        level = [
            [210, 32, 500, 500],
            [210, 32, 200, 400],
            [210, 32, 600, 300],
        ]

        # перебор массива и добавление каждой платформы в группу спрайтов
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# основная функция программы
def main():
    # инициализация
    pygame.init()

    # установка высоты и ширины
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # название игры
    pygame.display.set_caption("Мой платформер 2д")

    # создание игрока
    player = Player()

    # создание уровней
    level_list = []
    level_list.append(Level_01(player))

    # устанавка текущего уровня
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # цикл, пока не будет нажата кнопка закрытия
    done = False

    # управление скоростью обновления экрана
    clock = pygame.time.Clock()

    # основной цикл программы
    while not done:
        # отслеживание действий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # если нажатие на стрелки клавиатуры, то движение объекта
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # обновление игрока
        active_sprite_list.update()

        # обновление объектов
        current_level.update()

        # если игрок приблизится к правой стороне, то дальше не двигается
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # если игрок приблизится к левой стороне, то дальше не двигается
        if player.rect.left < 0:
            player.rect.left = 0

        # рисование объектов на окне
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # устанавка количества фреймов
        clock.tick(45)

        # обновление экрана после рисования объектов
        pygame.display.flip()

    # закрытие программы
    pygame.quit()

if __name__ == "__main__":
    main()