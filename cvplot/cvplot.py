import ipywidgets as widgets
from traitlets import Unicode, Dict, List
from sklearn.exceptions import NotFittedError
from joblib import delayed, Parallel, cpu_count
import numpy as np
import pandas as pd
from .sensitivity_analysis import SensitivityAnalysis
from tqdm.notebook import tqdm
import sys
from .lime import LIMEExplainer, trapezoid_pdf
from functools import partial

# See js/lib/cvplot.js for the frontend counterpart to this file.

@widgets.register
class CVPlot(widgets.DOMWidget):
  # Name of the widget view class in front-end
  _view_name = Unicode('View').tag(sync=True)

  # Name of the widget model class in front-end
  _model_name = Unicode('Model').tag(sync=True)

  # Name of the front-end module containing widget view
  _view_module = Unicode('cvplot').tag(sync=True)

  # Name of the front-end module containing widget model
  _model_module = Unicode('cvplot').tag(sync=True)

  # Version of the front-end module containing widget view
  _view_module_version = Unicode('^0.1.0').tag(sync=True)
  # Version of the front-end module containing widget model
  _model_module_version = Unicode('^0.1.0').tag(sync=True)

  value = Dict().tag(sync=True)
  selection = List().tag(sync=True)

  def __init__(self, X, y, features, model, explainer=None, target_index=0, max=500, **kwargs):
    super().__init__(**kwargs)

    if not isinstance(X, pd.DataFrame):
      raise Exception("Please provide X as a DataFrame, such that it includes feature names (`columns`).")

    try:
      model.predict(True)
    except NotFittedError as e:
      raise Exception("Provided model not fitted")
    except:
      pass

    if not (hasattr(model, 'predict_proba') and callable(getattr(model, 'predict_proba'))):
      raise Exception("Classifier requires a method 'predict_proba(X)'")

    if explainer is not None and not callable(explainer):
      raise Exception("Argument 'explainer' needs to be None, or a function returning a feature contribution score for every feature of the provided instance.")

    if explainer is None:
      lime = LIMEExplainer(
        X,
        distance_kernel=partial(trapezoid_pdf, 1, 1),
        categorical_features={},
        scale=True,
        sample_size=1000
      )

      def explainer(instance):
        return lime.explain_instance(
            np.asanyarray(instance).reshape(1,-1),
            model.predict_proba, 
            kernel_width=0.5, 
            labels=(target_index,)
          )[0][0]

    self.X = X
    self.y = y

    self.target_index = target_index
    self.features = features
    self.model = model
    self.expainer = explainer

    X = X.iloc[0:max,:]
    y = np.asanyarray(y)[0:max]

    def kernel(instances, fi):
      return [
        explainer(instance)[fi]
        for instance in instances
      ]

    sa = SensitivityAnalysis(X, kernel)

    # intermediate = [
    #   sa.sa_multiple_features(instance, features=features)
    #   for instance in tqdm(np.asanyarray(X), leave=False, file=sys.stdout)
    # ]
    fn = delayed(partial(sa.sa_multiple_features, features=features))
    iterator = tqdm(np.asanyarray(X), leave=False, file=sys.stdout)
    intermediate = Parallel(n_jobs=cpu_count())(fn(i) for i in iterator)

    cvlines = {
      f: [x[f].tolist() for x in intermediate]
      for f in features
    }

    contributions = [explainer(x) for x in np.asanyarray(X)]

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    self.value = {
      'contributions': np.asanyarray(cvlines).tolist(),
      'contributions2': np.asanyarray(contributions).tolist(),
      'values': np.asanyarray(X[features]).tolist(),
      'features': list(features),
      'y': np.asanyarray(y).tolist(),
      'yhat': np.asanyarray(probabilities).tolist(),
      'predictions': np.asanyarray(predictions).tolist(),
      'classes': np.unique(y).tolist(),
    }