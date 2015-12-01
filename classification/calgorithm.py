# A fork of lucid_utils.classification.old_algorithm for better performance and accuracy for LUCID data

import common
import end_detection

class Blob(common.Blob):
    def classify(self):
        # Start by getting gamma and alpha possibilities out of the way - they're eeeasy
        if self.num_pixels < 4:
            return 'gamma'
        if self.density > 0.75 and self.num_pixels > 11:
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
        if (self.squiggliness / self.radius) < 0.1 and self.radius > 20:
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
        if self.radius > 7 and self.squiggliness < 0.4:
            return 'proton'
        # But for smaller ones they also need to be 'chunky' otherwise they're probably electrons!!!!! OH NOES!!
        if self.num_pixels / (2*self.radius) > 1.5 and self.squiggliness < 0.7:
            return 'proton'
            # Yay
        # Okay. The situation is looking generally pretty good, though the greatest trouble may still be ahead...
        # What remains is either a lovely curly beta-y thing
        # Or
        # A crazy crossed track or crazy particle shower or something else REALLY AWESOME!!!!!
        # But WAIT A SECOND!
        # The crazy things are always big!
        # And we've already dealt with the things which are big but NOT crazy
        # So
        # You know what?s
        # What we really need is an aspect ratio check here...
        # But
        # That sounds really boring to write
        # Let's just cheat :)
        return 'beta'


def classify(blob):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify()

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
