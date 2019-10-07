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
SmallEnemies = 3
SmallEnemyHP = 30
MediumEnemies = 3
MediumEnemyHP = 60
LargeEnemies = 3
LargeEnemyHP = 100

#Score Variables
HIT_SCORE = 10
KillScoreS = 50
KillScoreM = 100
KillScoreL = 150

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/laserBlue1.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/PlayerBlue.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

#Small Enemy
class EnemyS(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/MeteorSmall1.png", 0.5)
        self.hp = SmallEnemyHP
        (self.center_x, self.center_y) = position

#Medium Enemy
class EnemyM(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/MeteorMedium1.png", 0.5)
        self.hp = MediumEnemyHP
        (self.center_x, self.center_y) = position

#Large Enemy
class EnemyL(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/MeteorLarge1.png", 0.5)
        self.hp = LargeEnemyHP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list_small = arcade.SpriteList()
        self.enemy_list_medium = arcade.SpriteList()
        self.enemy_list_large = arcade.SpriteList()
        self.player = Player()
        self.score = 0

#Enemy setup
    def setup(self):
        for i in range(SmallEnemies):
            xs = 175 
            ys = 500 * (i+1) - 40
            enemyS = EnemyS((xs,ys))
            self.enemy_list_small.append(enemyS)

        for i in range(MediumEnemies):
            xm = 375
            ym = 500 * (i+1) - 40
            enemyM = EnemyM((xm,ym))
            self.enemy_list_medium.append(enemyM)

        for i in range(LargeEnemies):
            xl = 625 
            yl = 500 * (i+1) - 40
            enemyL = EnemyL((xl,yl))
            self.enemy_list_large.append(enemyL)


    def update(self, delta_time):
        self.bullet_list.update()

        #Small Kill and Score
        self.enemy_list_small.update()
        for e in self.enemy_list_small:
            hit = arcade.check_for_collision_with_list(e, self.bullet_list)
            for h in hit:
                e.hp = e.hp - h.damage
                self.score += HIT_SCORE
                h.kill()
                if e.hp <=0:
                    e.kill()
                    self.score += KillScoreS

        #Medium Kill and Score
        self.enemy_list_medium.update()
        for e in self.enemy_list_medium:
            hit = arcade.check_for_collision_with_list(e, self.bullet_list)
            for h in hit:
                e.hp = e.hp - h.damage
                self.score += HIT_SCORE
                h.kill()
                if e.hp <=0:
                    e.kill()
                    self.score += KillScoreM

        #Large Kill and Score
        self.enemy_list_large.update()
        for e in self.enemy_list_large:
            hit = arcade.check_for_collision_with_list(e, self.bullet_list)
            for h in hit:
                e.hp = e.hp - h.damage
                self.score += HIT_SCORE
                h.kill()
                if e.hp <=0:
                    e.kill()
                    self.score += KillScoreL

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list_large.draw()
        self.enemy_list_medium.draw()
        self.enemy_list_small.draw()

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