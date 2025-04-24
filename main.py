#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import argparse




class Mechanism:
    def __init__(self, filepath, ylabel='kcal/mol', saveshow_plot = True, plot_color = 'k', show_plot = True, skip_zero = False, custom_zero = 0, legend_name = 'asd', yscaling = 1.2):
        self.file_location = filepath
        self.skip_first_line = True
        self.ylabel = ylabel
        self.plot_color = plot_color
        self.yscaling = yscaling
        self.show_plot = show_plot
        self.skip_zero = skip_zero
        self.legend_name = legend_name
        self.custom_zero = custom_zero
        self.saveshow_plot = saveshow_plot

        Mechanism.load_file(self)
        if skip_zero:
            self.energies = self.energies-custom_zero
        else:
            Mechanism.zero_energies(self)
        Mechanism.prepare_lines(self)
        # Mechanism.make_plot(self)

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


        # print(x)
        # print(y)

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
            # print(n)
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
    def make_plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(6,4),dpi=150)
        for line, y_line in zip(self.x_state, self.y_state):
            ax.plot(line, y_line, color=self.plot_color)
        for line, y_line in zip(self.x_reaction, self.y_reaction):
            ax.plot(line, y_line, f'{self.plot_color}--')
        for xt, yt, st in zip(self.x_text, self.y_text,self.labels):
            # st = str(st)
            plt.text( xt, yt, st, va = 'center',  ha= 'center', color = self.plot_color)
        a = plt.gca()
        min, max = a.get_ylim()
        #usually the text does not fit into the frame so i extend it my yscaling, default 1.2 i.e. 20% in total

        new_min, new_max = scale_axis(min, max, self.yscaling)

        ax.plot([],[],color=self.plot_color, label = self.legend_name)
        ax.set_ylim(new_min,new_max) # extend by
        ax.set_ylabel(self.ylabel, fontsize = 16)# 10% to include the text
        ax.set_xticks([])
        ax.set_xlabel('Reaction Coordinate', fontsize = 14)
        if self.saveshow_plot:
            plt.savefig('mechanism.svg')
            plt.show()


def scale_axis(min, max, scaling):
    center = (max + min) / 2
    dist_to_max = max - center
    dist_to_max = dist_to_max * scaling
    new_max = center + dist_to_max
    new_min = center - dist_to_max
    return new_min, new_max



def find_lowest_energy(file_names, skip_first_line = True):
    all_energies = []
    starting_energies = []
    for file_n in file_names:
        with open(file_n, 'r') as file:
            lines = file.readlines()


        for i, line in enumerate(lines):
            if skip_first_line and i == 0:
                continue
            label, energy = line.split(',')
            energy = energy.replace('\n', '').replace(' ', '')
            energy = float(energy)
            if skip_first_line:
                if i == 1:
                    starting_energies.append(energy)
            else:
                if i == 0:
                    starting_energies.append(energy)


            all_energies.append(energy)
    starting_energies = np.array(starting_energies)
    all_energies = np.array(all_energies)
    zero = starting_energies.min()
    min = all_energies.min() - starting_energies.min()
    max = all_energies.max() - starting_energies.min()
    return zero, min, max

# find_lowest_energy(['example.txt','example2.txt','example3.txt', ])

def multi_figure(N_plots, file_names = [],  legend_labels = [], scaling=1.2):

    assert len(file_names) == len(legend_labels)
    assert len(file_names) == len(plot_colors)
    plot_colors = ['k', 'b', 'r', 'g'][:N_plots]

    zero, min, max = find_lowest_energy(file_names)
    # N_plots = len(file_names)
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    for i in range(N_plots):
        pi = Mechanism(file_names[i], '$\Delta G$ (kcal/mol)', saveshow_plot = False, legend_name=legend_labels[i], plot_color = plot_colors[i], skip_zero=True, custom_zero=zero)
        pi.make_plot(ax=ax)

    nmin, nmax = scale_axis(min, max, scaling)

    ax.set_ylim(nmin, nmax)
    ax.legend(loc = [1.1, 0.2])
    plt.tight_layout()
    plt.savefig('mechanism.svg')
    plt.show()




def main():
    parser = argparse.ArgumentParser(description="""This a program to make (multiple or single) reaction mechanism from 
                                                 Gibbs free energys for single only the input file is required:
                                                  replot -f example.txt
                                                  for multi plots we need number of plots, plot labels for the legend and 
                                                  input files
                                                  replot -n 3 -fn example1.txt,example2.txt,exampl3.txt, -ln Singlet,Triplet,Quintet
                                                  
                                                  
                                                  input files should be structured like:
                                                  
                                                  first line ignored
                                                  label1, energy1,
                                                  label2, energy2,
                                                  label3, energy3,..
                                                  
                                                  It is assumed that the odd ones are minima and even ones are TS's
                                                  but it only change the placement of label which can/should be fixed 
                                                  with some svg editor anyway (like inkscape)
                                                  """)
    parser.add_argument("-n", type=int, help="Number of spinstates to consider", default='1', required=False)
    parser.add_argument("-f", type=str, help="Filename or other string input", required=False)

    args = parser.parse_args()

    print(f"number of axes in ploy: {args.n} filename:'{args.f}'")

    if args.n > 1:
        multi_figure(args.n, file_names=['example.txt', 'example2.txt', 'example3.txt'],
                     legend_labels=['Singlet', 'Triplet', 'Quintet'], plot_colors=['k', 'b', 'r'])
    else:
        Mechanism('example3.txt', saveshow_plot = True).make_plot()


# single figure

if __name__ == "__main__":
    main()

