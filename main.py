import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image, ImageTk
import itertools


def index_image_colors(image_path, num_colors=4):
    image = Image.open(image_path).convert('RGB')
    data = np.array(image)
    reshaped_data = data.reshape((-1, 3))

    model = KMeans(n_clusters=num_colors)
    labels = model.fit_predict(reshaped_data)
    palette = model.cluster_centers_.astype('uint8')

    indexed_data = np.array([palette[label] for label in labels])
    indexed_image = Image.fromarray(indexed_data.reshape(data.shape), 'RGB')

    return indexed_image, palette, labels.reshape(data.shape[:-1])


def generate_color_permutations(palette):
    return list(itertools.permutations(palette))


def recolor_image_gzhel(labels, gzhel_palette):
    recolored_data = np.zeros(
        (labels.shape[0], labels.shape[1], 3), dtype=np.uint8)

    for index, color in enumerate(gzhel_palette):
        recolored_data[labels == index] = color

    recolored_image = Image.fromarray(recolored_data, 'RGB')
    return recolored_image


# Палитра цветов
gzhel_palette = [
    (248, 250, 252),  # Белый
    (150, 172, 217),   # Голубой
    (67, 94, 170),     # Синий
    (56, 70, 126),      # Темно-синий
]


def select_source_image():
    file_path = filedialog.askopenfilename()
    entry_source_path.delete(0, tk.END)
    entry_source_path.insert(0, file_path)


def select_destination_folder():
    folder_path = filedialog.askdirectory()
    entry_destination_path.delete(0, tk.END)
    entry_destination_path.insert(0, folder_path)


def index_and_recolor_images():
    source_image_path = entry_source_path.get()
    destination_folder_path = entry_destination_path.get()

    if not source_image_path or not destination_folder_path:
        messagebox.showwarning(
            "Внимание", "Пожалуйста, укажите исходный файл и папку назначения.")
        return

    try:
        indexed_image, original_palette, labels = index_image_colors(
            source_image_path)
        gzhel_permutations = generate_color_permutations(gzhel_palette)

        for i, permutation in enumerate(gzhel_permutations):
            recolored_image = recolor_image_gzhel(labels, permutation)
            recolored_image.save(
                f'{destination_folder_path}/recolored_image_gzhel_{i}.png')

        messagebox.showinfo(
            "Успешно", "Изображение успешно проиндексировано и перекрашено.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def open_explanatory_popup():
    messagebox.showinfo("Для чего нужна эта программа?",
                        "Программа предназначена для работы с изображениями, преобразуя их цветовую палитру "
                        "в соответствии с заданной схемой, и в данном случае это палитра Гжель – традиционный "
                        "русский стиль росписи, использующий оттенки синего на белом фоне.\n\n"
                        "Использование программы:\n"
                        "• Запустите программу. В главном окне вы увидите интерфейс с кнопками и полями "
                        "для выбора изображения и папки назначения.\n"
                        "• С помощью кнопок \"Выберите исходное изображение\" и \"Выберите папку назначения\" "
                        "укажите необходимые пути.\n"
                        "• После выбора нажмите кнопку \"Перекрасить!\", чтобы начать процесс индексации и перекраски.\n"
                        "• Программа отобразит сообщение об успешном завершении процесса или сообщение об ошибке, "
                        "если что-то пойдет не так.")


root = tk.Tk()
# Используйте тему оформления 'clam'
style = ttk.Style(root)
style.theme_use('clam')

# Определите кастомные шрифты и цвета
customFont = ('Roboto', 16)
buttonFont = ('Roboto', 16, 'bold')
backgroundColor = '#CFDEFF'
buttonColor = '#d0d0f0'
textColor = '#333'

# Настройте корневое окно
root.configure(bg=backgroundColor)
root.title("Колорирование в палитру Гжели")

pic = Image.open('pic.png')
pic = pic.resize((300, 300))

question = Image.open('question.png')
question = question.resize((50, 50))


pic_image = ImageTk.PhotoImage(pic)
question_image = ImageTk.PhotoImage(question)
palette_image = tk.PhotoImage(file='palette.png')

pic_label = tk.Label(root, image=pic_image, bg=backgroundColor)
palette_label = tk.Label(root, image=palette_image)

pic_label.pack(padx=20, pady=10)

frame = tk.Frame(root, bg=backgroundColor)
frame.pack(padx=20, pady=20)

label_source_path = tk.Label(frame, text="Путь к исходному изображению:",
                             bg=backgroundColor, fg=textColor, font=customFont)
label_source_path.pack(fill='x', expand=True, pady=(0, 10))

entry_source_path = tk.Entry(frame, font=customFont)
entry_source_path.pack(fill='x', expand=True)

button_browse_source = tk.Button(
    frame, text="Выбрать", command=select_source_image, bg=buttonColor, font=buttonFont)
button_browse_source.pack(fill='x', expand=True, pady=5)

label_destination_path = tk.Label(
    frame, text="Путь к папке назначения:", bg=backgroundColor, fg=textColor, font=customFont)
label_destination_path.pack(fill='x', expand=True, pady=(10, 10))

entry_destination_path = tk.Entry(frame, font=customFont)
entry_destination_path.pack(fill='x', expand=True)

button_browse_destination = tk.Button(
    frame, text="Выбрать", command=select_destination_folder, bg=buttonColor, font=buttonFont)
button_browse_destination.pack(fill='x', expand=True, pady=5)

button_recolor = tk.Button(
    frame, text="Перекрасить!", command=index_and_recolor_images, bg=buttonColor, font=buttonFont)
button_recolor.pack(fill='x', expand=True, pady=(30, 15))

palette_label.pack(padx=20, pady=10)

question_button = tk.Button(
    root, image=question_image, command=open_explanatory_popup, background=backgroundColor, border=0)
question_button.pack(padx=20, pady=20)


root.mainloop()
