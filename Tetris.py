import pygame
import random

pygame.font.init()

s_x = 800
s_y = 700
širina_igre = 300  
visina_igre = 600  
veličina_bloka = 30

gornji_lijevi_x = (s_x - širina_igre) // 2
gornji_lijevi_y = s_y - visina_igre


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

oblici = [S, Z, I, O, J, L, T]
oblici_boje = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Figura(object):  
    def __init__(self, x, y, oblik):
        self.x = x
        self.y = y
        self.oblik = oblik
        self.boja = oblici_boje[oblici.index(oblik)]
        self.rotacija = 0


def napraviti_grid(fiskna_pozicija={}): 
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in fiskna_pozicija:
                c = fiskna_pozicija[(j,i)]
                grid[i][j] = c
    return grid


def okretanje_oblika(oblik):
    pozicije = []
    format = oblik.oblik[oblik.rotacija % len(oblik.oblik)]

    for i, linija in enumerate(format):
        red = list(linija)
        for j, kolona in enumerate(red):
            if kolona == '0':
                pozicije.append((oblik.x + j, oblik.y + i))

    for i, pos in enumerate(pozicije):
        pozicije[i] = (pos[0] - 2, pos[1] - 4)

    return pozicije


def provjera_kretnje(oblik, grid):
    dozvoljena_pozicija = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    dozvoljena_pozicija = [j for sub in dozvoljena_pozicija for j in sub]

    formatted = okretanje_oblika(oblik)

    for pos in formatted:
        if pos not in dozvoljena_pozicija:
            if pos[1] > -1:
                return False
    return True


def izgubiti(pozicije):
    for pos in pozicije:
        x, y = pos
        if y < 1:
            return True

    return False


def preuzmi_oblik():
    return Figura(5, 0, random.choice(oblici))


def glavni_text(površina, text, size, boja):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, boja)

    površina.blit(label, (gornji_lijevi_x + širina_igre /2 - (label.get_width()/2), gornji_lijevi_y + visina_igre/2 - label.get_height()/2))


def prikazi_grid(površina, grid):
    sx = gornji_lijevi_x
    sy = gornji_lijevi_y

    for i in range(len(grid)):
        pygame.draw.line(površina, (128,128,128), (sx, sy + i*veličina_bloka), (sx+širina_igre, sy+ i*veličina_bloka))
        for j in range(len(grid[i])):
            pygame.draw.line(površina, (128, 128, 128), (sx + j*veličina_bloka, sy),(sx + j*veličina_bloka, sy + visina_igre))


def očistiti_redove(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        red = grid[i]
        if (0,0,0) not in red:
            inc += 1
            ind = i
            for j in range(len(red)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def prikazati_sljedeci_oblik(oblik, površina):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Sljedeći oblik', 1, (255,255,255))

    sx = gornji_lijevi_x + širina_igre + 50
    sy = gornji_lijevi_y + visina_igre/2 - 80
    format = oblik.oblik[oblik.rotacija % len(oblik.oblik)]

    for i, linija in enumerate(format):
        red = list(linija)
        for j, kolona in enumerate(red):
            if kolona == '0':
                pygame.draw.rect(površina, oblik.boja, (sx + j*veličina_bloka, sy + i*veličina_bloka, veličina_bloka, veličina_bloka), 0)

    površina.blit(label, (sx + 10, sy - 50))


def ažuriranje_rezultata(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def prikaži_prozor(površina, grid, score=0, prethodni_high_score = 0):
    površina.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    površina.blit(label, (gornji_lijevi_x + širina_igre / 2 - (label.get_width() / 2), 30))


    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = gornji_lijevi_x + širina_igre + 50
    sy = gornji_lijevi_y + visina_igre/2 - 100

    površina.blit(label, (sx + 20, sy + 160))

    label = font.render('High Score: ' + prethodni_high_score, 1, (255,255,255))

    sx = gornji_lijevi_x - 200
    sy = gornji_lijevi_y + 200

    površina.blit(label, (sx - 40 , sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(površina, grid[i][j], (gornji_lijevi_x + j*veličina_bloka, gornji_lijevi_y + i*veličina_bloka, veličina_bloka, veličina_bloka), 0)

    pygame.draw.rect(površina, (255, 0, 0), (gornji_lijevi_x, gornji_lijevi_y, širina_igre, visina_igre), 5)

    prikazi_grid(površina, grid)



def main(win):  
    prethodni_high_score = max_score()
    fiksne_pozicije = {}
    grid = napraviti_grid(fiksne_pozicije)

    promjeni_oblik = False
    run = True
    trenutni_oblik = preuzmi_oblik()
    sljedeći_oblik = preuzmi_oblik()
    clock = pygame.time.Clock()
    vrijeme_pada = 0
    brzina_pada = 0.27
    vrijeme_levela = 0
    score = 0

    while run:
        grid = napraviti_grid(fiksne_pozicije)
        vrijeme_pada += clock.get_rawtime()
        vrijeme_levela += clock.get_rawtime()
        clock.tick()

        if vrijeme_levela/1000 > 5:
            vrijeme_levela = 0
            if vrijeme_levela > 0.12:
                vrijeme_levela -= 0.005

        if vrijeme_pada/1000 > brzina_pada:
            vrijeme_pada = 0
            trenutni_oblik.y += 1
            if not(provjera_kretnje(trenutni_oblik, grid)) and trenutni_oblik.y > 0:
                trenutni_oblik.y -= 1
                promjeni_oblik = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    trenutni_oblik.x -= 1
                    if not(provjera_kretnje(trenutni_oblik, grid)):
                        trenutni_oblik.x += 1
                if event.key == pygame.K_RIGHT:
                    trenutni_oblik.x += 1
                    if not(provjera_kretnje(trenutni_oblik, grid)):
                        trenutni_oblik.x -= 1
                if event.key == pygame.K_DOWN:
                    trenutni_oblik.y += 1
                    if not(provjera_kretnje(trenutni_oblik, grid)):
                        trenutni_oblik.y -= 1
                if event.key == pygame.K_UP:
                    trenutni_oblik.rotacija += 1
                    if not(provjera_kretnje(trenutni_oblik, grid)):
                        trenutni_oblik.rotacija -= 1
                if event.key == pygame.K_SPACE:
                   while provjera_kretnje(trenutni_oblik, grid):
                    trenutni_oblik.y += 1
                   trenutni_oblik.y -= 1
                   print(okretanje_oblika(trenutni_oblik))

        oblik_pos = okretanje_oblika(trenutni_oblik)

        for i in range(len(oblik_pos)):
            x, y = oblik_pos[i]
            if y > -1:
                grid[y][x] = trenutni_oblik.boja

        if promjeni_oblik:
            for pos in oblik_pos:
                p = (pos[0], pos[1])
                fiksne_pozicije[p] = trenutni_oblik.boja
            trenutni_oblik = sljedeći_oblik
            sljedeći_oblik = preuzmi_oblik()
            promjeni_oblik = False
            score += očistiti_redove(grid, fiksne_pozicije) * 10

        prikaži_prozor(win, grid, score, prethodni_high_score)
        prikazati_sljedeci_oblik(sljedeći_oblik, win)
        pygame.display.update()

        if izgubiti(fiksne_pozicije):
            glavni_text(win, "Izgubio si", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            ažuriranje_rezultata(score)


def main_menu(win):  
    run = True
    while run:
        win.fill((0,0,0))
        glavni_text(win, 'Pritisnite dugme da započnete', 40, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_x, s_y))
pygame.display.set_caption('Tetris')
main_menu(win)