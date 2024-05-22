import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image
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


# Создание интерфейса
root = tk.Tk()
root.title("Колорирование в палитру Гжели")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_source_path = tk.Label(frame, text="Путь к исходному изображению:")
label_source_path.pack(fill='x', expand=True)

entry_source_path = tk.Entry(frame, width=50)
entry_source_path.pack(fill='x', expand=True)

button_browse_source = tk.Button(
    frame, text="Выбрать", command=select_source_image)
button_browse_source.pack(fill='x', expand=True)

label_destination_path = tk.Label(frame, text="Путь к папке назначения:")
label_destination_path.pack(fill='x', expand=True)

entry_destination_path = tk.Entry(frame, width=50)
entry_destination_path.pack(fill='x', expand=True)

button_browse_destination = tk.Button(
    frame, text="Выбрать", command=select_destination_folder)
button_browse_destination.pack(fill='x', expand=True)

button_recolor = tk.Button(
    frame, text="Перекрасить!", command=index_and_recolor_images)
button_recolor.pack(fill='x', expand=True)

root.mainloop()
