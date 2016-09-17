# AUTHOR: Cal Hewitt

try:
    import common
except ImportError:
    from . import common

class Blob(common.Blob):
    def classify(self):
        # Start by eliminating a few trivial cases - if a blob has fewer than 4 pixels, then it must be a gamma (or there is no way of telling otherwise)
        if self.num_pixels < 4:
            return 'gamma'
        if self.num_pixels < 8:
            return 'beta' # protons always leave more of a splash
        if (self.density > 0.75 and self.num_pixels > 11) or (self.avg_neighbours > 6 and self.curvature_radius > 8):
            return 'alpha'
        if (self.line_residual / self.radius) < 0.1 and self.radius > 40:
            # Straight clusters over a certain radius will always be caused by a muon
            return 'muon'
            # Knock Knock
            # Who's there?
            # Interrupting physicist.
            # Interrupting physicist wh--
            # MUUUUUUUUON
        if ((self.curvature_radius > 50 or self.line_residual < self.circle_residual) and self.width > 1.5) or self.avg_neighbours > 3.5:
            return 'proton'
        else:
            return 'beta'

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
