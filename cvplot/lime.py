from bisect import bisect
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import normalize, MinMaxScaler
from sklearn.utils import check_random_state


class LIMEExplainer(object):
  def __init__(self, training_data, scale=True, distance_kernel=None, sample_size=5000, categorical_features=None, random_state=None):
    """Instantiates the explainer, and creates hypersphere samples for estimation

    Parameters
    ----------
    training_data: numpy.array (2d)
      Training data for the reference model. Categorical variables should be encoded as integers.

    distance_kernel: Callable
      PDF function defining the distance kernel. Should at least take one argument.

    sample_size: Int
      Number of points to sample within the hypersphere.

    categorical_features: [[int]]
      List indexes of categorical features in training_data.

    random_state: Int
      Optional seed for random choices.

    """
    self.random_state = check_random_state(random_state)
    np.random.seed(random_state)

    # allow pandas dataframe, or np array with one-hot encoded categorical features.
    self.training_data = np.asanyarray(training_data)
    self.categorical_features = categorical_features if categorical_features is not None else []
    self.sample_size = sample_size

    if scale:
      #self.scaler = StandardScaler(with_mean=True)
      self.scaler = MinMaxScaler()
      self.scaler.fit(training_data)

      for index in self.categorical_features:
        self.scaler.min_[index] = 0
        self.scaler.scale_[index] = 1
    else:
      self.scaler = None

    # Create hypersphere samples.
    self.n_categorical = len(self.categorical_features)
    self.n_numerical = training_data.shape[1] - self.n_categorical
    self.cat_idx = list(self.categorical_features.keys())

    if distance_kernel is None:
      self.distance_kernel = np.vectorize(lambda x: x ** (1 / self.n_numerical))
    else:
      accounted_kernel = lambda x: distance_kernel(x) * (x ** (self.n_numerical - 1))
      self.distance_kernel = np.vectorize(self._transform(accounted_kernel, self.n_numerical))

  @property
  def surrogate(self):
    """ Yield the surrogate model """
    try:
      return self._surrogate
    except AttributeError:
      self._surrogate = Ridge(alpha=1, fit_intercept=True, random_state=self.random_state)
      return self._surrogate

  @property
  def distance_kernel(self):
    return self._distance_kernel

  @distance_kernel.setter
  def distance_kernel(self, value):
    """ Set distance kernel and generate transfer dataset (sphere) as a side effect. """
    accounted_kernel = lambda x: value(x) * (x ** (self.n_numerical - 1))
    self._distance_kernel = np.vectorize(self._transform(accounted_kernel, self.n_numerical))

    if self.n_numerical > 0:
      sphere = np.random.normal(size=(self.sample_size, self.n_numerical))
      sphere = normalize(sphere)
      sphere *= self._distance_kernel(np.random.uniform(size=self.sample_size)).reshape(-1,1) / 2
    else:
      sphere = np.zeros(shape=(0, self.sample_size))

    for index in self.categorical_features:
      categories, frequencies = np.unique(self.training_data[:, index], return_counts=True)
      values = self.random_state.choice(categories, size=self.sample_size, replace=True, p=frequencies / float(sum(frequencies)))
      sphere = np.insert(sphere, index, values, axis=1)

    self.sphere = sphere

  def explain_instance(self, instance, predict_fn, kernel_width=0.5, labels=(0,), surrogate=None):
    """Explain the instance.

    Parameters
    ----------
    instance: numpy.array (2d)
      Instance to be explained. Should match the columns of the provided training data (so categorical variables
      one-hot encoded)

    predict_fn: Callable
      Predict function of the model to approximate.

    kernel_width: float
      Size of the region of interest, as a fraction of the normalized feature space width. 1 means a spherical region
      that touches min and max of every feature.

    labels: tuple
      Indexes of classes to show explanation from. Defaults to the first class.

    surrogate: (sklearn.base.BaseEstimator, sklearn.base.RegressorMixin)
      Surrogate model to train. Should at least conform to BaseEstimator and RegressorMixin.

    Returns
    -------
    [([float], float)]
      Returns an array of results (one for each class). Every results is a tuple of feature contributions (one for each
      feature) and a R^2 score for the fit.

    """
    surrogate = surrogate or self.surrogate

    # Create transfer dataset by permuting the original instance with the hypersphere samples
    if self.scaler is not None:
      instance = self.scaler.transform(instance)

    scalar = [1 if i in self.cat_idx else kernel_width for i in range(instance.shape[1])]
    X_transfer = scalar * self.sphere
    X_transfer += [0 if i in self.cat_idx else val for i, val in enumerate(instance[0])]

    for index in self.categorical_features:
      X_transfer[:,index] = (X_transfer[:,index] == instance[:,index]).astype(int)

    y_transfer = predict_fn(self.scaler.inverse_transform(X_transfer) if self.scaler is not None else X_transfer)

    def explain_label(label):
      surrogate.fit(X_transfer, y_transfer[:, label])
      score = surrogate.score(X_transfer, y_transfer[:, label])
      return surrogate.coef_, score

    return [explain_label(label) for label in labels]

  """
  Transforms a PDF into an inverse CDF for sampling.
  """
  def _transform(self, pdf, dimensions, sample_size = 1000):
    # Approximate cumulative distribution function
    cdf_samples = np.array([pdf(x) for x in np.linspace(0, 1, sample_size)])
    cdf_samples = np.cumsum(cdf_samples)
    cdf_samples /= cdf_samples[-1]

    # Return inverse of cdf
    return lambda y: bisect(cdf_samples, y) / sample_size

def trapezoid_pdf(x, a, b):
  if 0 <= x and  x <= a:
    return (2 / (a + b))
  elif a <= x and x <= b:
    return (2 / (a + b)) * ((b - x) / (b - a))
  else:
    return 0

def exponential_pdf(x, kernel_width):
  return np.sqrt(np.exp(-(x ** 2) / kernel_width ** 2))
