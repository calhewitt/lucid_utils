try:
    import common
except ImportError:
    from . import common

class Blob(common.Blob):
    def classify(self):
        return [self.num_pixels, self.density, self.radius, self.curvature_radius, self.line_residual, self.circle_residual, self.width, self.avg_neighbours]

def classify(blob):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify()

def classify_masked(blob):
    # Method for early LUCID data where half of pixels are masked:
    b = Blob(blob)
    b.density *= 2
    b.width *= 2
    return b.classify()
