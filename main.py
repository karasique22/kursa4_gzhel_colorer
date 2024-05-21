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


gzhel_palette = [
    (248, 250, 252),  # Белый
    (150, 172, 217),   # Голубой
    (67, 94, 170),     # Синий
    (56, 70, 126),      # Темной-синий
]


image_path = 'kotenok.png'
indexed_image, original_palette, labels = index_image_colors(image_path)

indexed_image.save('indexed_image.png')

gzhel_permutations = generate_color_permutations(gzhel_palette)

for i, permutation in enumerate(gzhel_permutations):
    recolored_image = recolor_image_gzhel(labels, permutation)
    recolored_image.save(f'recolored_image_gzhel_{i}.png')
