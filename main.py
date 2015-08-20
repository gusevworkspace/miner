#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #demo: miner
# #by Dmitry Gusev
# #dep: random
#
import os,random
import logging



# Logging
LOG_FORMAT= '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
logging.basicConfig(format=LOG_FORMAT, level = logging.INFO)

legend = {"bomb":"B",
          "flag":"F",
          0:".",
          1:'1',
          2:'2',
          3:'3',
          4:'4',
          5:'5',
          6:'6',
          7:'7',
          8:'8'
          }

near_coordinates=[[1,1],
                  [1,0],
                  [1,-1],
                  [0,-1],
                  [-1,-1],
                  [-1,0],
                  [-1,1],
                  [0,1]
                  ]
class Cell(object):
    def __init__(self):
        self.is_revealed = False
        self.is_flaged = False
        self.is_bomb = False
        self.bombs_near = 0
        self.label = ' '
        logging.debug("Объект Ячейка сгененирован")

    def __repr__(self):
        if self.is_flaged:
            return legend["flag"]
        else:
            return self.label

    def make_flaged(self):
        if not self.is_revealed:
            self.is_flaged = not self.is_flaged
            logging.debug("Флаг снят/поставлен")
        else:
            logging.debug("Поле уже открыто. Нечего тут ставить")

    def plant_bomb(self):
        if not self.is_bomb:
            self.is_bomb = True
            return True
        else:
            return False

    def reveal(self):
        if self.is_revealed:
            logging.info("Клетка уже открыта")
            return 1
        if self.is_flaged:
            logging.info("Следует снячала снять флаг")
            return 2
        if self.is_bomb:
            self.label=legend['bomb']
            logging.info("BOOM!")
            return 3
        if 0 <= self.bombs_near <= 8:
            self.is_revealed = True
            self.label=legend[self.bombs_near]
            return 0

class Board(object):
    def __init__(self, size_X, size_Y):
        self.size_X=int(size_X)
        self.size_Y=int(size_Y)
        self.created = False
        self.mined = False
        logging.debug("Объект Поле создан")

    def generate_field(self):
        self.field = []
        for y in range(self.size_Y):
            field_string = [Cell() for count in range(self.size_X)]
            logging.debug(field_string)
            self.field.append(field_string)
        self.created = True
        logging.debug("Поле сгенерированно")

    def print_field(self):
        # Header
        print '/' +"-"*3*self.size_X + '\\'
        for i in self.field:
            print '|'+str(i)+'|'
        print '\\' +"-"*3*self.size_X + '/'


    def mine_board(self, num_mines):
        if not self.created or self.mined:
            logging.error("Не получилось заминировать поле")
            return 1
        self.num_mines=num_mines
        mines=0
        while self.num_mines != mines:
            # Генерируем координаты мины
            rand_x=random.randint(0,self.size_X-1)
            rand_y=random.randint(0,self.size_Y-1)
            if not self.field[rand_y][rand_x].plant_bomb():
                logging.debug("Мина уже лежит в точке (%s,%s)" % (rand_x,rand_y))
            else:
                logging.info("Мину положили в точке (%s,%s)" % (rand_x,rand_y))
                mines += 1
                logging.debug("Осталось положить %s мин" % (self.num_mines - mines))

    def count_bombs_near(self,x,y):
        for c in near_coordinates:
            if 0 <= x+c[0] < self.size_X \
                    and 0 <= y+c[1] < self.size_Y:
                if self.field[y+c[1]][x+c[0]].is_bomb:
                    self.field[y][x].bombs_near += 1

    def reveal_near(self,x,y):
        for c in near_coordinates:
#            a=raw_input("(%s,%s) %s" % (x,y,c))
            if 0 <= x+c[0] < self.size_X \
              and 0 <= y+c[1] < self.size_Y \
              and not self.field[y+c[1]][x+c[0]].is_revealed:
                self.reveal_board_cell(x+c[0],y+c[1])

    def num_board(self):
        for x in range(0,self.size_X):
            for y in range(0,self.size_Y):
                self.count_bombs_near(x,y)
                logging.debug("В округе (%s,%s) %s мин" % (x,y,self.field[y][x].bombs_near))

    def reveal_board_cell(self,x,y):
        res = self.field[y][x].reveal()
        if self.field[y][x].bombs_near == 0:
            self.reveal_near(x,y)
        if res == 3:
            self.print_field()
            print("Напоролся на бомбу. Игра окончена")
            return False
        return True

    def flag_cell(self,x,y):
        self.field[y][x].make_flaged()
        self.print_field()

    def check_board(self):
        logging.debug("Инициализирована проверка неоткрытых клеток")
        for x in range(0,self.size_X):
            for y in range(0,self.size_Y):
                if not self.field[y][x].is_revealed and not self.field[y][x].is_bomb:
                    logging.debug("Клетка (%s,%s) еще не открыта" % (x,y))
                    return False
        return True

F = Board(8,6)
F.generate_field()
F.mine_board(4)
F.num_board()
F.print_field()

while True:
    F.print_field()
    print("Ваши действия:\n1) Открыть\n2) Поставить/снять флаг")
    ans = raw_input()
    if ans == 'q':
        break
    if ans == '1':
        x=int(raw_input('X: '))
        y=int(raw_input('Y: '))
        os.system('clear')
        if not F.reveal_board_cell(x,y):
            break
        if F.check_board():
            print("Ура, все пустые поля раскрыты!")
            break
    if ans == '2':
        x=int(raw_input('X: '))
        y=int(raw_input('Y: '))
        os.system('clear')
        F.flag_cell(x,y)
