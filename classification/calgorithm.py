# AUTHOR: Cal Hewitt
# An alternative analysis strategy based on the same metrics (calculated in common.py) as earlier algorithms
# A 'mode' can be specified as an argument to the classify function - this can either be
# (i) MODE_LUCID - Prioritise the distinction between protons and electrons - this can be done with much more accuracy
#   than previous algorithms, though this still has a habit of misclassifying some betas
# (ii) MODE_CERNATSCHOOL - Classify ONLY alpha, beta and gamma, though this is very accurate with these particle types
# Generally, the algorithm will classify 'agressively', ie. never returning a 'not sure' verdict - this is useful
# for generating counts for mapping with LUCID data.
# TODO develop separate modes for lower 'agression' settings
# Sorry about snarky commenting. Will be removed soon.

import common
import end_detection

class Blob(common.Blob):
    def classify(self, mode):
        if not mode in ["MODE_LUCID", "MODE_CERNATSCHOOL"]:
            raise Exception("Invalid mode name, cannot continue")
        # Start by getting gamma and alpha possibilities out of the way - they're eeeasy
        if self.num_pixels < 4:
            return 'gamma'
        if (self.density > 0.75 and self.num_pixels > 7) or (self.radius < 9 and self.num_pixels > 90):
            return 'alpha'
        if self.num_pixels > 9 and self.num_pixels / (self.radius*2) > 2:
            return 'alpha'
        # Must be beta, proton, muon or other.
        # We've narrowed it down to one of the long, straight ones - result, eh?
        # Aren't we clever?
        # Right, let's get rid of small betas, these can't really be anything else
        if self.num_pixels < 6 or self.radius < 2:
            return 'beta'
        # Whoop whoop!
        # Right, let's now move on to the really straight long ones.
        # They're either going to be protons or muons, and which of the two can be worked out from their length
        # Anyway, enough talk for now. Let's do some CODING!!!!!
        if (self.squiggliness / self.radius) < 0.1 and self.radius > 20 and mode == "MODE_LUCID":
            # Well, well, well then.
            # The REALLY BIG ones are probably muons
            # So
            return 'muon'
            # Knock Knock
            # Who's there?
            # Interrupting physicist.
            # Interrupting physicist wh--
            # MUUUUUUUUON
        # Otherwise, a kind of protonic designation seems in order
        # The big ones only need be long and straigt...
        if self.radius > 7 and self.squiggliness < 0.4 and mode == "MODE_LUCID":
            return 'proton'
        # But for smaller ones they also need to be 'chunky' otherwise they're probably electrons!!!!! OH NOES!!
        if self.num_pixels / (2*self.radius) > 1.5 and self.squiggliness < 0.7 and mode == "MODE_LUCID":
            return 'proton'
            # Yay
        # Okay. The situation is looking generally pretty good, though the greatest trouble may still be ahead...
        # What remains will either be
        # (a) A standard beta
        # (b) Crossed tracks / an interaction / or a particle shower
        # Let's first get the possiblity of a small simple beta out of the way...
        if self.radius < 10 or mode == "MODE_CERNATSCHOOL":
            # No real way to work more out about these
            return 'beta'
        # TODO an end detection check here - algorithm too slow at the moment for general use, so cheating :)
        return 'beta'


def classify(blob, mode="MODE_LUCID"):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify(mode)

def classify_multiple(blobs):
    classifications = []
    for blob in blobs:
        classifications.append(classify(blob))
    return classifications

def classify_masked(blob):
    # Method for early LUCID data where half of pixels are masked:
    b = Blob(blob)
    b.num_pixels *= 2
    b.density *= 2
    return b.classify()
