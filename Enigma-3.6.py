#das boot укажет на энигму
#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#что было будет, что будет было
#тысяча лет в двенадцати годах
#U в пучинах
from permutation import Permutation
from dataclasses import dataclass, field
from itertools import *
import customtkinter as CTk
from CTkTable import *
from typing_extensions import Self
@dataclass
class rotor():
    turn = 0
    links = ()

class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title('ENIGMA')
        self.geometry('800x400')
        self.resizable(width= 'FALSE', height= 'FALSE')

        self.input_text_frame = CTk.CTkLabel(master = self,text = 'Text to encrypt:', width= 100, height= 20)
        self.input_text_frame.grid(row = 0, column = 0, padx=(10,20), pady =(10,20), sticky = "ew" )
        self.to_input_text_frame = CTk.CTkEntry(master = self, width= 200, height= 20, placeholder_text = 'your text')
        self.to_input_text_frame.grid(row = 0, column = 1, padx=(10,20),pady =(10,20), sticky = "ew",columnspan = 2 )
        self.button_to_start = CTk.CTkButton(self, text ='Encrypt/decrypt',fg_color = 'orange', text_color = 'dark blue', width = 50, height = 20, command = self.start_code_by_button)
        self.button_to_start.grid(row = 0, column = 3,padx=(10,20),pady =(10,20), sticky = "ew" )
        self.export_text = CTk.CTkTextbox(master = self, width= 200, height= 20,)
        self.export_text.grid(row = 1, column = 0, padx=(10,20),pady =(10,20), sticky = "nsew", columnspan =4)

        self.third_code = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '3-rd let.') # три ячейки ввода начального положения роторов
        self.third_code.grid(row = 3, column = 4, padx=(10,20),pady =(10,20), sticky = "ew" )
        self.second_code = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '2-nd let.')
        self.second_code.grid(row = 3, column = 5, padx=(10,20),pady =(10,20), sticky = "ew")
        self.first_code = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '1-st let.')
        self.first_code.grid(row = 3, column = 6, padx=(10,20),pady =(10,20), sticky = "ew")
        self.code_text = CTk.CTkLabel(master = self, width= 60, height= 20, text = 'Select the starting position of the rotors')
        self.code_text.grid(row = 3, column = 0, padx=(10,20),pady =(10,20), sticky = "ew", columnspan = 4)

        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #алфавит, в теории можно использовать и любой другой

        self.rotor1 = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '1-st rot.') # три ячейки ввода расположения роторов.
        self.rotor1.grid(row = 2, column = 6, padx=(10,20),pady =(10,20), sticky = "ew" )
        self.rotor2 = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '2-nd rot.')
        self.rotor2.grid(row = 2, column = 5, padx=(10,20),pady =(10,20), sticky = "ew")
        self.rotor3 = CTk.CTkEntry(master = self, width= 60, height= 20, placeholder_text = '3-rd rot.')
        self.rotor3.grid(row = 2, column = 4, padx=(10,20),pady =(10,20), sticky = "ew")
        self.rotors_text = CTk.CTkLabel(master = self, width= 60, height= 20, text = 'There are rotors A-C. Choose the order of rotors')
        self.rotors_text.grid(row = 2, column = 0, padx=(10,20),pady =(10,20), sticky = "ew", columnspan = 4)

        self.rotor_A = rotor()
        self.rotor_B = rotor()
        self.rotor_C = rotor()
        self.rotor_A.links = Permutation(5,11,13,6,12,7,3,17,22,26,14,20,15,23,25,8,24,21,19,16,1,9,2,18,4,10) # у роторов должны быть циклические перестановки
        self.rotor_B.links = Permutation(1,10,4,11,19,9,18,21,24,2,12,8,23,20,13,3,17,7,26,14,16,25,6,22,15,5)
        self.rotor_C.links = Permutation(2,4,6,8,10,12,3,16,18,20,24,22,26,14,25,5,9,23,7,1,11,13,21,19,17,15)
        self.rotors_dict = { #словарь роторов, для выбора порядка расположения ротора 
        'A': self.rotor_A,
        'B': self.rotor_B,
        'C': self.rotor_C}
        
        self.first_rotor = rotor() #порядрк расположение роторов при работе шифровальной машины
        self.second_rotor = rotor()
        self.second_rotor = rotor()

        self.reflector = Permutation(25,18,21,8,17,19,12,4,16,24,14,7,15,11,13,9,5,2,6,26,3,23,22,10,1,20) # у рефлектора (и коммутатора) попарные соответствия
        self.commutation_panel = Permutation(8,2,14,4,16,6,20,1,9,10,12,11,13,3,15,5,17,18,19,7,21,26,23,24,25,22)# в данной настройке комутационной панели соединения: AH, CN, EP, GT, KL, VZ

    def start_code_by_button(self):
        self.main_part()
    def from_letter_to_number(self, letter): # по нужной букве находим её порядковый номер в нашем алфавите
        number = self.abc.index(letter) + 1
        return(number)

    def from_number_to_letter(self,number): #по нужному порядковому номеру в алфавите находим букву
        for i in self.abc:
            if self.abc.index(i) == number - 1:
                letter = i
        return(letter)

    def turn_by_one(self, rotor_to_turn): #функция проворта ротора на одно значение
        if rotor_to_turn.turn < len(self.abc) - 1:
            rotor_to_turn.turn += 1
        elif rotor_to_turn.turn == len(self.abc) - 1:
            rotor_to_turn.turn = 0

    #ротор до подсчёта - может быть выход комм.панели или выход рефлектора, ротор после подсчёта - может быть вход рефлектора или входом ком.панели
    #при обратном прохождениии ротор до и ротор после меняются местами
    #ротор до и ротор после - это значения их оборотов (максимум = на 1 меньше длины алфавита)
    def real_position_counter(self,number_to_count, rotor_before_count, rotor_after_count): 
        if  number_to_count + rotor_after_count - rotor_before_count <= 0:
            counted_number = number_to_count + rotor_after_count - rotor_before_count + len(self.abc)       
        elif number_to_count + rotor_after_count - rotor_before_count > len(self.abc):
            counted_number = number_to_count + rotor_after_count - rotor_before_count - len(self.abc)
        else:    
            counted_number = number_to_count + rotor_after_count - rotor_before_count
        return (counted_number)

    def main_part(self):
        """
        Стоит отметить, что роторо first-third расположены в порядке прохождения сигнала, однако, поскольку в оригинальной машине значения начального положения роторов устанавливались слева направо,
        а сигнал проходил справа налево, то создаётся путаница
        Для примера:
        Первый ротор - правый
        Второй ротор - центральный
        Третий ротор - левый
        
        Положение: III II I
        Ротор:      B  A  C
        Позиция:    V  S  E
        В таком случае первый ротор по прохожению сигнала будет ротор С c начальной позицией E, второй ротор — ротор A с начальной позицией S и третий ротор по прохождению сигнала - ротор B с позициецй V.

        Таким образом, если записывать не по их расположению в реальной машине а по прохождению сигнала, то будет:
        Положение:  I II III
        Ротор:      C  A  B
        Позиция:    E  S  V
        """
        self.first_rotor = self.rotors_dict.get(self.rotor1.get().upper()) #выбор порядка расположения роторов
        self.second_rotor = self.rotors_dict.get(self.rotor2.get().upper()) 
        self.third_rotor = self.rotors_dict.get(self.rotor3.get().upper()) 

        self.first_rotor.turn = self.from_letter_to_number(self.first_code.get()) - 1 #выставление значения шифра на роторе
        self.second_rotor.turn = self.from_letter_to_number(self.second_code.get()) - 1
        self.third_rotor.turn = self.from_letter_to_number(self.third_code.get()) - 1

        self.text_to_enigma = self.to_input_text_frame.get() #текст на зашифровку/расшифровку. Набирать без пробелов заглавными буквами английского алфавита (26шт)
        self.text_from_enigma = ''
        self.first_rotor_turn_count = 0
        self.second_rotor_turn_count = 0
        for i in self.text_to_enigma:
            self.to_first_rotor = 0
            self.turn_by_one(self.first_rotor)
            self.first_rotor_turn_count +=1
            if self.first_rotor_turn_count == len(self.abc):
                self.first_rotor_turn_count = 0
                self.turn_by_one(self.second_rotor)
                self.second_rotor_turn_count += 1
            
            if self.second_rotor_turn_count == len(self.abc):
                self.second_rotor_turn_count = 0
                self.turn_by_one(self.third_rotor)  

            i_number = self.from_letter_to_number(i)
            inter_number = self.commutation_panel(i_number)
            inter_number = self.real_position_counter(inter_number, 0, self.first_rotor.turn) #переход с комм. панели на 1 ротор, оборот комм понели = const = 0
            inter_number = self.first_rotor.links(inter_number) # трансформация внутри первого ротора
            inter_number = self.real_position_counter(inter_number, self.first_rotor.turn, self.second_rotor.turn) #переход с первого ротора на второй ротор
            inter_number = self.second_rotor.links(inter_number)# трансформация внутри второго ротора
            inter_number = self.real_position_counter(inter_number, self.second_rotor.turn, self.third_rotor.turn) #переход со второго ротора на третий ротор
            inter_number = self.third_rotor.links(inter_number)# трансформация внутри третьего ротора

            inter_number = self.real_position_counter(inter_number, self.third_rotor.turn, 0) #с 3 ротора на рефлектор
            inter_number = self.reflector(inter_number) #проход через рефлектор

            inter_number = self.real_position_counter(inter_number, 0, self.third_rotor.turn) #с рефлектора на 3 ротор
            inter_number = self.third_rotor.links.inverse()(inter_number) #преобразования в 3 роторе
            inter_number = self.real_position_counter(inter_number, self.third_rotor.turn,self.second_rotor.turn ) #с 3 ротора на 2 ротор
            inter_number = self.second_rotor.links.inverse()(inter_number) #преоразования на 2 роторе
            inter_number = self.real_position_counter(inter_number, self.second_rotor.turn, self.first_rotor.turn)# с 2 ротора на 1 ротор
            inter_number = self.first_rotor.links.inverse()(inter_number) #преобразования на 1 роторе
            inter_number = self.real_position_counter(inter_number, self.first_rotor.turn, 0)# с 1 ротора на ком. панель
            inter_number = self.commutation_panel.inverse()(inter_number)
            self.text_from_enigma += self.from_number_to_letter(inter_number)

        self.export_text.delete('0.0','end') #очистка поля выводного текста
        self.export_text.insert('0.0',self.text_from_enigma) #запись в поле нового текста
if __name__ == '__main__':
    app = App()
    
    app.mainloop()
