import numpy as np
from functools import partial


class SensitivityAnalysis:
  def __init__(self, X, kernel):
    self.X = X
    self.kernel = kernel

  def get_grid_points(self, instance, fi, num_samples=20):
    """
    Generates a line of instances on a line spanning the marginal distribution
    of the chosen feature.

    Parameters
    ----------
    instance: pd.Series
        The instance that needs to be perturbed.

    fi: int
        Index of feature to apply sensitivity analysis on.

    num_samples: int
        Number of samples taken along the marginal distribution of the feature.

    Returns
    -------
    instances: numpy.ndarray
        List of instances with the chosen feature varying along its marginal
        distribution.

    """
    feature_range = (self.X.iloc[:,fi].min(), self.X.iloc[:,fi].max())
    values = np.linspace(feature_range[0], feature_range[1], num_samples)

    instance = np.asanyarray(instance)
    if len(instance.shape) != 2:
      instance = instance.reshape(1, -1)
    instances = np.repeat(np.asanyarray(instance), len(values), axis=0)
    instances[:, fi] = values

    return instances

  def sa(self, instance, fi, num_samples=20):
    """
    Perform sensitivity analysis for single instance and single feature

    Parameters
    ----------
    instance: pd.Series
        The instance that needs to be perturbed.

    fi: int
        Index of feature to apply sensitivity analysis on.

    num_samples: int
        Number of samples taken along the marginal distribution of the feature.

    Returns
    -------
    line: numpy.ndarray
        Array of values along the line of sensitivity analysis.
    """
    points = self.get_grid_points(instance, fi, num_samples=num_samples)
    kernel = partial(self.kernel, fi=fi)
    return np.array([points[:,fi], kernel(points)]).T

  def sa_multiple_features(self, instance, features, num_samples=20):
    """
    Perform sensitivity analysis for single instance on multiple features.

    Parameters
    ----------
    instance: pd.Series
        The instance that needs to be perturbed.

    features: array<str>
        Names of the columns to apply sensitivity analysis on, as used in the 
        dataset DataFrame columns.

    num_samples: int
        Number of samples taken along the marginal distribution of the feature.

    Returns
    -------
    line: dict
        Dictionary of sensitivity analysis lines for every feature.
    """
    return {
      feature: self.sa(instance, list(self.X.columns).index(feature), num_samples=num_samples)
      for feature in features
    }