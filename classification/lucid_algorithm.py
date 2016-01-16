# AUTHOR: Cal Hewitt
# An alternative analysis strategy based on the same metrics (calculated in common.py) as earlier algorithms
# A 'mode' can be specified as an argument to the classify function - this can either be
# (i) MODE_LUCID - Prioritise the distinction between protons and electrons - this can be done with much more accuracy
#   than previous algorithms, though this still has a habit of misclassifying some betas
# (ii) MODE_CERNATSCHOOL - Classify ONLY alpha, beta and gamma, though this is very accurate with these particle types
# Generally, the algorithm will classify 'agressively', ie. never returning a 'not sure' verdict - this is useful
# for generating counts for mapping with LUCID data.
# TODO develop separate modes for lower 'agression' settings

import common

class Blob(common.Blob):
    def classify(self, mode):
        if not mode in ["MODE_LUCID", "MODE_CERNATSCHOOL"]:
            raise Exception("Invalid mode name, cannot continue")
        # Start by eliminating a few trivial cases - if a blob has fewer than 4 pixels, then it must be a gamma (or there is no way of telling otherwise)
        if self.num_pixels < 4:
            return 'gamma'
        # Large clusters with such a high density, or smaller ones with even higher densities are always alpha
        if (self.density > 0.75 and self.num_pixels > 7) or (self.radius < 9 and self.num_pixels > 90):
            return 'alpha'
        # By this stage, must be beta, proton, muon or other.
        # Very small clusters will always be electron hits
        if self.num_pixels < 6 or self.radius < 2:
            return 'beta'
        # Whoop whoop!
        if (self.squiggliness / self.radius) < 0.1 and self.radius > 40 and mode == "MODE_LUCID":
            # Straight clusters over a certain radius will always be caused by a muon
            return 'muon'
            # Knock Knock
            # Who's there?
            # Interrupting physicist.
            # Interrupting physicist wh--
            # MUUUUUUUUON
        # Otherwise, if the cluster is nearly completly straight it is probably a proton
        if self.radius > 7 and self.squiggliness < 0.4 and mode == "MODE_LUCID":
            return 'proton'
        # Shorter proton tracks can be distinguished from straight betas on their 'chunkiness'; the average width of the track
        if self.num_pixels / (2*self.radius) > 1.5 and self.squiggliness < 0.7 and mode == "MODE_LUCID":
            return 'proton'
        if self.radius < 10 or mode == "MODE_CERNATSCHOOL":
            # If classifying aggressively, the only remaining possibility is a beta particle
            return 'beta'
        # TODO an end detection check here - algorithm too slow at the moment for general use, so cheating
        # Want to be able to distinguish boring betas from interesting events or interactions
        return 'beta'
        # More coming soon!


def classify(blob, mode="MODE_LUCID"):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify(mode)

def classify_masked(blob, mode="MODE_LUCID"):
    # Method for early LUCID data where half of pixels are masked:
    b = Blob(blob)
    b.num_pixels *= 2
    b.density *= 2
    return b.classify(mode)
