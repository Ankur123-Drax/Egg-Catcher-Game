from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, PhotoImage

canvas_width = 800
canvas_height = 400
root = Tk()
root.title('Egg Catcher Game')
photo = PhotoImage(file = "icon/eggIcon.png")
root.iconphoto(False, photo)
c = Canvas(root, width=canvas_width, height=canvas_height, background="#FFE5B4")
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill="sea green", width=0)
c.create_oval(-80, -80, 120, 120, fill='turquoise3', width=0)
c.pack()

color_cycle = cycle(["light blue", "light green", "pink", "light yellow", "cyan","white"])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty = 0.95

catcher_image = PhotoImage(file="image/basket.png")
catcher_width = catcher_image.width()
catcher_height = catcher_image.height()
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20

catcher = c.create_image(catcher_startx, catcher_starty, anchor='nw', image=catcher_image)
game_font = font.nametofont("TkFixedFont")
game_font.config(size=19)

score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="black", text="Score: " + str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor="ne", font=game_font, fill="black",
                           text="Lives: " + str(lives_remaining))

eggs = []

def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: " + str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))

def check_catch():
    (catcherx, catchery) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx + catcher_width and catchery < eggy2 < catchery + catcher_height:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: " + str(score))

def move_left(event):
    (x, y) = c.coords(catcher)
    if x > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x, y) = c.coords(catcher)
    if x + catcher_width < canvas_width:
        c.move(catcher, 20, 0)

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()
