# AUTHOR: Cal Hewitt
# An alternative analysis strategy based on the same metrics (calculated in common.py) as earlier algorithms
# A 'mode' can be specified as an argument to the classify function - this can either be
# (i) MODE_LUCID - Prioritise the distinction between protons and electrons - this can be done with much more accuracy
#   than previous algorithms, though this still has a habit of misclassifying some betas
# (ii) MODE_CERNATSCHOOL - Classify ONLY alpha, beta and gamma, though this is very accurate with these particle types
# Generally, the algorithm will classify 'agressively', ie. never returning a 'not sure' verdict - this is useful
# for generating counts for mapping with LUCID data.
# TODO develop separate modes for lower 'agression' settings

try:
    import common
except ImportError:
    from . import common

class Blob(common.Blob):
    def classify(self, mode):
        if not mode in ["MODE_LUCID", "MODE_CERNATSCHOOL"]:
            raise Exception("Invalid mode name, cannot continue")
        # Start by eliminating a few trivial cases - if a blob has fewer than 4 pixels, then it must be a gamma (or there is no way of telling otherwise)
        if self.num_pixels < 4:
            return 'gamma'
        if (self.density > 0.75 and self.num_pixels > 11):
            return 'alpha'
        if (self.line_residual / self.radius) < 0.1 and self.radius > 40 and mode == "MODE_LUCID":
            # Straight clusters over a certain radius will always be caused by a muon
            return 'muon'
            # Knock Knock
            # Who's there?
            # Interrupting physicist.
            # Interrupting physicist wh--
            # MUUUUUUUUON
        if (self.curvature_radius > 50 or self.line_residual < self.circle_residual) and self.width > 1.5:
            return 'proton'
        else:
            return 'beta'

def classify(blob, mode="MODE_LUCID"):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify(mode)

def classify_masked(blob, mode="MODE_LUCID"):
    # Method for early LUCID data where half of pixels are masked:
    b = Blob(blob)
    b.density *= 2
    b.width *= 2
    return b.classify(mode)
