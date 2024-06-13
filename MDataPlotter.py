import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import matplotlib.pyplot as plt
import os
import webbrowser

class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MData Plotter")
        self.create_widgets()
        self.dados_convertidos = []
        self.arquivos = []
        self.cores = []
        self.estilos = []
        self.nomes = []
        self.inverter_colunas = []
        self.eixo_x = ""
        self.eixo_y = ""
        self.titulo_grafico = ""
        self.definir_valores_eixos = tk.BooleanVar()
        self.x_min = tk.DoubleVar()
        self.x_max = tk.DoubleVar()
        self.x_interval = tk.DoubleVar()
        self.y_min = tk.DoubleVar()
        self.y_max = tk.DoubleVar()
        self.y_interval = tk.DoubleVar()

    def create_widgets(self):
        # Arte ASCII
        ascii_art = """
╥━━━━━━━━╭━━╮━━━━━━━━━━━━━┳
╢╭╮╭━━━━━┫┃▋▋━▅     ━━━━━━━   ┣
╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫     ┊  Esse é o ┊┣
╢╰━┫┈┈┈┈┈╰╯╰┳━╯     ┊  Cão Max┊┣
╢┊┊┃┏┳┳━━┓┏┳┫┊┊        ━━━━━━━  ┣
╨━━┗┛┗┛━━┗┛┗┛━━━━━━━━━━━━━┻
"""
        tk.Label(self.root, text=ascii_art, justify=tk.LEFT).pack()

        # Frame for number of files and submit button
        num_files_frame = tk.Frame(self.root)
        num_files_frame.pack(pady=5)

        self.num_files_label = tk.Label(num_files_frame, text="Quantos arquivos deseja ler? (Máximo 6)")
        self.num_files_label.pack()

        self.num_files_entry = tk.Entry(num_files_frame, width=3)
        self.num_files_entry.pack()

        self.submit_num_files_button = tk.Button(num_files_frame, text="Submeter", command=self.select_files)
        self.submit_num_files_button.pack(pady=5)

        # Frame for buttons in the second row
        second_row_frame = tk.Frame(self.root)
        second_row_frame.pack(pady=5)

        self.edit_options_button = tk.Button(second_row_frame, text="Editar", command=self.get_options, state=tk.DISABLED)
        self.edit_options_button.pack(side=tk.LEFT, padx=5)

        self.plot_button = tk.Button(second_row_frame, text="Plotar Gráficos", command=self.plotar_graficos, state=tk.DISABLED)
        self.plot_button.pack(side=tk.LEFT, padx=5)

    def select_files(self):
        try:
            num_arquivos = int(self.num_files_entry.get())
            if num_arquivos < 1 or num_arquivos > 6:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido entre 1 e 6.")
            return
        
        self.arquivos = []
        for i in range(num_arquivos):
            arquivo = filedialog.askopenfilename(title=f"Selecione o arquivo {i+1}", filetypes=[("Text files", "*.txt"), ("Data files", "*.dat"), ("XY files", "*.xy")])
            if arquivo:
                self.arquivos.append(arquivo)
            else:
                messagebox.showwarning("Atenção", "Nenhum arquivo foi fornecido.")
                return
        
        self.get_options()
        
    def get_options(self):
        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Opções de Personalização")

        # Adiciona um canvas e uma scrollbar
        canvas = tk.Canvas(self.options_window)
        scrollbar = tk.Scrollbar(self.options_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.options = []

        for i, arquivo in enumerate(self.arquivos):
            frame = tk.Frame(scrollable_frame)
            frame.pack(padx=10, pady=10)

            nome_arquivo = os.path.basename(arquivo)

            tk.Label(frame, text=f"Arquivo: {nome_arquivo}", anchor="center").pack()

            cor_label = tk.Label(frame, text="Cor", anchor="center")
            cor_label.pack()
            cor_entry = tk.Entry(frame)
            cor_entry.pack()
            cor_entry.insert(0, self.cores[i] if i < len(self.cores) else '')

            estilo_label = tk.Label(frame, text="Código do Marcador", anchor="center")
            estilo_label.pack()
            estilo_entry = tk.Entry(frame)
            estilo_entry.pack()
            estilo_entry.insert(0, self.estilos[i] if i < len(self.estilos) else '')

            nome_label = tk.Label(frame, text="Legenda das linhas", anchor="center")
            nome_label.pack()
            nome_entry = tk.Entry(frame)
            nome_entry.pack()
            nome_entry.insert(0, self.nomes[i] if i < len(self.nomes) else '')

            inverter_var = tk.BooleanVar()
            inverter_var.set(self.inverter_colunas[i] if i < len(self.inverter_colunas) else False)
            inverter_check = tk.Checkbutton(frame, text="Deseja inverter as colunas do arquivo?", variable=inverter_var, anchor="center")
            inverter_check.pack()

            self.options.append((arquivo, cor_entry, estilo_entry, nome_entry, inverter_var))

        eixo_x_label = tk.Label(scrollable_frame, text="Nome do eixo X:", anchor="center")
        eixo_x_label.pack()
        self.eixo_x_entry = tk.Entry(scrollable_frame)
        self.eixo_x_entry.pack()
        self.eixo_x_entry.insert(0, self.eixo_x)

        eixo_y_label = tk.Label(scrollable_frame, text="Nome do eixo Y:", anchor="center")
        eixo_y_label.pack()
        self.eixo_y_entry = tk.Entry(scrollable_frame)
        self.eixo_y_entry.pack()
        self.eixo_y_entry.insert(0, self.eixo_y)

        titulo_label = tk.Label(scrollable_frame, text="Título do gráfico:", anchor="center")
        titulo_label.pack()
        self.titulo_entry = tk.Entry(scrollable_frame)
        self.titulo_entry.pack()
        self.titulo_entry.insert(0, self.titulo_grafico)

        definir_eixos_check = tk.Checkbutton(scrollable_frame, text="Definir os valores dos eixos?", variable=self.definir_valores_eixos, command=self.toggle_axis_popup, anchor="center")
        definir_eixos_check.pack()

        tk.Button(scrollable_frame, text="Matplot Códigos de Marcador", command=self.open_marker_codes).pack(pady=5)
        tk.Button(scrollable_frame, text="Submeter Opções", command=self.process_options).pack()

    def toggle_axis_popup(self):
        if self.definir_valores_eixos.get():
            self.show_axis_popup()
        elif hasattr(self, 'axis_popup'):
            self.axis_popup.destroy()

    def show_axis_popup(self):
        self.axis_popup = tk.Toplevel(self.root)
        self.axis_popup.title("Definir Valores do Eixo")

        tk.Label(self.axis_popup, text="X Min:").grid(row=0, column=0)
        self.x_min_entry = tk.Entry(self.axis_popup, textvariable=self.x_min)
        self.x_min_entry.grid(row=0, column=1)

        tk.Label(self.axis_popup, text="X Max:").grid(row=1, column=0)
        self.x_max_entry = tk.Entry(self.axis_popup, textvariable=self.x_max)
        self.x_max_entry.grid(row=1, column=1)

        tk.Label(self.axis_popup, text="X Intervalo:").grid(row=2, column=0)
        self.x_interval_entry = tk.Entry(self.axis_popup, textvariable=self.x_interval)
        self.x_interval_entry.grid(row=2, column=1)

        tk.Label(self.axis_popup, text="Y Min:").grid(row=3, column=0)
        self.y_min_entry = tk.Entry(self.axis_popup, textvariable=self.y_min)
        self.y_min_entry.grid(row=3, column=1)

        tk.Label(self.axis_popup, text="Y Max:").grid(row=4, column=0)
        self.y_max_entry = tk.Entry(self.axis_popup, textvariable=self.y_max)
        self.y_max_entry.grid(row=4, column=1)

        tk.Label(self.axis_popup, text="Y Intervalo:").grid(row=5, column=0)
        self.y_interval_entry = tk.Entry(self.axis_popup, textvariable=self.y_interval)
        self.y_interval_entry.grid(row=5, column=1)

        tk.Button(self.axis_popup, text="OK", command=self.axis_popup.destroy).grid(row=6, columnspan=2)

    def process_options(self):
        self.dados_convertidos = []
        for arquivo, cor_entry, estilo_entry, nome_entry, inverter_var in self.options:
            dados = self.ler_dados_arquivo(arquivo)
            if inverter_var.get():
                col1, col2 = self.troca_colunas(dados)
            else:
                linhas = dados.strip().split('\n')
                col1, col2 = zip(*(linha.split() for linha in linhas))
                col1 = [v.replace(',', '.') for v in col1]
                col2 = [v.replace(',', '.') for v in col2]
            self.dados_convertidos.append((col1, col2))

        self.cores = [entry[1].get() for entry in self.options]
        self.estilos = [entry[2].get() for entry in self.options]
        self.nomes = [entry[3].get() for entry in self.options]
        self.inverter_colunas = [entry[4].get() for entry in self.options]
        self.eixo_x = self.eixo_x_entry.get()
        self.eixo_y = self.eixo_y_entry.get()
        self.titulo_grafico = self.titulo_entry.get()

        self.options_window.destroy()
        self.plot_button.config(state=tk.NORMAL)
        self.edit_options_button.config(state=tk.NORMAL)

    def ler_dados_arquivo(self, arquivo):
        with open(arquivo, 'r') as f:
            dados = f.read()
        return dados

    def troca_colunas(self, dados):
        linhas = dados.strip().split('\n')
        col1 = []
        col2 = []
        for linha in linhas:
            valores = linha.split()
            col1.append(valores[1].replace(',', '.'))
            col2.append(valores[0].replace(',', '.'))
        return col1, col2

    def plotar_graficos(self):
        dados_plot = []
        for (col1, col2) in self.dados_convertidos:
            x = list(map(float, col1))
            y = list(map(float, col2))
            dados_plot.append((x, y))

        self.plotar_dados(dados_plot, self.cores, self.estilos, self.nomes, self.eixo_x, self.eixo_y, self.titulo_grafico)

    def plotar_dados(self, dados, cores, marcadores, nomes, eixo_x, eixo_y, titulo):
        fig, ax = plt.subplots(figsize=(10, 6))  # Cria uma figura com um gráfico

        for (x, y), cor, marcador, nome in zip(dados, cores, marcadores, nomes):
            ax.plot(x, y, label=nome, color=cor, marker=marcador)
            ax.set_xlabel(eixo_x)
            ax.set_ylabel(eixo_y)
            ax.set_title(titulo)
            ax.legend()

            if self.definir_valores_eixos.get():
                ax.set_xlim(self.x_min.get(), self.x_max.get())
                ax.set_ylim(self.y_min.get(), self.y_max.get())
                ax.set_xticks([self.x_min.get() + i * self.x_interval.get() for i in range(int((self.x_max.get() - self.x_min.get()) // self.x_interval.get()) + 1)])
                ax.set_yticks([self.y_min.get() + i * self.y_interval.get() for i in range(int((self.y_max.get() - self.y_min.get()) // self.y_interval.get()) + 1)])

        plt.tight_layout()
        plt.show()

    def open_marker_codes(self):
        webbrowser.open("https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()

