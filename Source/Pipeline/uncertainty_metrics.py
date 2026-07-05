import numpy as np
import itertools
import arviz as az
from scipy.stats import entropy

def intervalOverlap(lowerI, upperI, lowerJ, upperJ):
        return (lowerI <= upperJ) and (lowerJ <= upperI)

def computeUncertainty(trace, regions):
    """
    Compute uncertainty metrics for the given trace and regions
    """

    nRegions = len(regions)

    samples = trace.posterior['beta'].values.reshape(-1, nRegions)

    rankings = np.argsort(-samples, axis=1)

    uniqueRankings, counts = np.unique(rankings, axis=0, return_counts=True)

    # Convert raw counts to proportions (that sum to 1)
    probabilities = counts / counts.sum()
    entropyValue = entropy(probabilities)

    flipProbabilities = dict()

    for regionI, regionJ in itertools.combinations(range(nRegions), 2):
        probIOverJ = (samples[:, regionI] > samples[:, regionJ]).mean()
        pairLabel = f'{regions[regionI]} over {regions[regionJ]}'
        flipProbabilities[pairLabel] = probIOverJ

    hdiBounds = az.hdi(trace, var_names=['beta'])

    hdiArray = hdiBounds['beta'].values

    hdiOverlaps = dict()

    for regionI, regionJ in itertools.combinations(range(nRegions), 2):
        lowerI, upperI = hdiArray[regionI]
        lowerJ, upperJ = hdiArray[regionJ]
        overlaps = intervalOverlap(lowerI, upperI, lowerJ, upperJ)
        pairLabel = f'{regions[regionI]} vs {regions[regionJ]}'
        hdiOverlaps[pairLabel] = overlaps

    return {
        'entropy': entropyValue,
        'flipProbabilities': flipProbabilities,
        'hdiOverlaps': hdiOverlaps
    }
    






    
    
   