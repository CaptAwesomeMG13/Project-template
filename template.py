import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Defender"
STARTING_LOCATION = (400,100)

#Bullet and Enemies Variables
BULLET_DAMAGE = 10
NUM_ENEMIES = 10
SmallEnemyHP = 30
MediumEnemyHP = 60
LargeEnemyHP = 100

#Score Variables
HIT_SCORE = 10
KillScoreS = 50
KillScoreM = 100
KillScoreL = 150

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/narwhal.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

#Small Enemy
class EnemyS(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/penguin.png", 0.5)
        self.hp = SmallEnemyHP
        (self.center_x, self.center_y) = position

#Medium Enemy
class EnemyM(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/penguin.png", 0.5)
        self.hp = MediumEnemyHP
        (self.center_x, self.center_y) = position

#Large Enemy
class EnemyL(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/penguin.png", 0.5)
        self.hp = LargeEnemyHP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0


    def setup(self):
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemyS = EnemyS((x,y))
            self.enemy_list.append(enemyS)   
            enemyM = EnemyM((x,y))
            self.enemy_list.append(enemyM)
            enemyL = EnemyL((x,y))
            self.enemy_list.append(enemyL)



    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            hit = arcade.check_for_collision_with_list(e, self.bullet_list)
            for h in hit:
                e.hp = e.hp - h.damage
                self.score += HIT_SCORE
                h.kill()
                if e.hp <=0:
                    if e == EnemyS:
                        self.score += KillScoreS
                    elif e == EnemyM:
                        self.score += KillScoreM
                    elif e == EnemyL:
                        self.score += KillScoreL

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()




    def on_mouse_motion(self, x, y, dx, dy):
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")

    def on_key_release(self, key, modifiers):
        """ 
        Called whenever a user releases a key. 
        """
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()