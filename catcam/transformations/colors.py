from sklearn.neighbors import BallTree


class ColorSchemeTransformer(object):
    def __init__(self, color_palette):
        self.color_mapper = BallTree(color_palette)

    def nearest_neighbors(self, image):
        flat_image = image.reshape((image.shape[0] * image.shape[1], 3)) 
        matched_colors = self.color_mapper.query(flat_image)[1]
        return matched_colors.reshape((image.shape[0], image.shape[1]))
