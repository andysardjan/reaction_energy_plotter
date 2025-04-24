
import matplotlib.pyplot as plt
import numpy as np




class Mechanism:
    def __init__(self, filepath, ylabel, yscaling = 1.2):
        self.file_location = filepath
        self.skip_first_line = True
        self.ylabel = ylabel
        self.yscaling = yscaling
        Mechanism.load_file(self)
        Mechanism.zero_energies(self)
        Mechanism.prepare_lines(self)
        Mechanism.make_plot(self)

    def load_file(self):
        with open(self.file_location, 'r') as file:
            lines = file.readlines()
        # print(lines)
        labels = []
        energies = []

        for i, line in enumerate(lines):
            if self.skip_first_line and i ==0:
                continue
            label, energy = line.split(',')
            energy = energy.replace('\n','').replace(' ','')
            energy = float(energy)
            energies.append(energy)
            labels.append(label)
        self.labels = labels
        self.energies = np.array(energies)
        return self

    def print_labels(self):
        print(self.labels)
        print(self.energies)
        return self

    def zero_energies(self):
        self.energies = self.energies - self.energies[0]
        return self

    def prepare_lines(self, width_reaction=1, width_state=0.5):
        x_state = []
        y_state= []
        x_reaction = []
        y_reaction = []

        x = []
        y = []
        x_text = []
        y_text = []

        for i, (l, e) in enumerate(zip(self.labels, self.energies)):
            x.append(i * width_reaction)
            x.append(i * width_reaction + width_state)
            y.append(e)
            y.append(e)


        print(x)
        print(y)

        # for i in range(len(x)):

        # x_state = x[0::2]
        # y_state = y[0::2]
        # x_reaction = x[1::2]
        # y_reaction = y[1::2]

        self.x_state = [x[i:i+2] for i in range(0, len(x), 2)]
        self.y_state = [y[i:i+2] for i in range(0, len(y), 2)]
        self.x_reaction = [x[i:i+2] for i in range(1, len(x)-1)]
        self.y_reaction = [y[i:i+2] for i in range(1, len(y)-1)]
        minmax_windows = self.energies.max()-self.energies.min()

        for n, (i,j)  in enumerate(zip(self.x_state, self.y_state)):
            print(n)
            x_avg = 1/2*(i[0] + i[1])

            if n%2 == 0:
                bump = - minmax_windows * 0.05
            else:
                bump = + minmax_windows * 0.05

            y_avg = 1/2*(j[0] + j[1]) + bump

            # print(x_avg)
            x_text.append(x_avg)
            y_text.append(y_avg)

        self.x_text = x_text
        self.y_text = y_text

        return self
    def make_plot(self):
        for line, y_line in zip(self.x_state, self.y_state):
            plt.plot(line, y_line, color='k')
        for line, y_line in zip(self.x_reaction, self.y_reaction):
            plt.plot(line, y_line, 'k--')
        for xt, yt, st in zip(self.x_text, self.y_text,self.labels):
            # st = str(st)
            plt.text( xt, yt, st, va = 'center',  ha= 'center')
        a = plt.gca()
        min, max = a.get_ylim()
        center = (max + min)/2
        dist_to_max = max - center
        dist_to_max = dist_to_max * self.yscaling
        new_max = center + dist_to_max
        new_min = center - dist_to_max
        plt.ylim(new_min,new_max) # extend by
        plt.ylabel(self.ylabel, fontsize = 16)# 10% to include the text
        plt.xticks([])
        plt.xlabel('Reaction Coordinate', fontsize = 14)
        plt.show()

Mechanism('example.txt', '$\Delta G$ (kcal/mol)')