"""Conditional-logit win model (the standard for horse racing: every race's runners compete
for one win, probabilities sum to 1 within the race).

Two stages (Benter's method):
  1. FORM model: weights for the pre-race features (predict.features), fitted on older races.
  2. COMBINED model: final score = a x form score + b x log(market chance), fitted on a
     LATER block of races, so the market blend is learned out of sample. The market already
     knows a lot; the form model only has to add what the market misses.
Kept separate for flat (turf + AW) and jumps.
"""
import numpy as np
from scipy.optimize import minimize

L2 = 1e-3


def _pack(samples):
    X, starts, won = [], [], []
    for s in samples:
        starts.append(len(X))
        won.append(len(X) + s[2])
        X.extend(s[1])
    return np.asarray(X, float), np.asarray(starts), np.asarray(won)


def _race_softmax(u, starts):
    m = np.maximum.reduceat(u, starts)
    lens = np.diff(np.append(starts, len(u)))
    e = np.exp(u - np.repeat(m, lens))
    z = np.add.reduceat(e, starts)
    return e / np.repeat(z, lens), m, z


def fit(X, starts, won):
    lens = np.diff(np.append(starts, len(X)))

    def nll(beta):
        u = X @ beta
        p, m, z = _race_softmax(u, starts)
        ll = u[won].sum() - (m + np.log(z)).sum()
        grad = X[won].sum(0) - (p[:, None] * X).sum(0)
        return -ll / len(starts) + L2 * beta @ beta, -grad / len(starts) + 2 * L2 * beta

    res = minimize(nll, np.zeros(X.shape[1]), jac=True, method="L-BFGS-B")
    return res.x


def probs(X, starts, beta):
    return _race_softmax(np.asarray(X, float) @ beta, starts)[0]


def form_scores(samples, beta):
    X, starts, _ = _pack(samples)
    return X @ beta, starts


def fit_form(samples):
    X, starts, won = _pack(samples)
    return fit(X, starts, won)


def combined_design(form_u, market):
    return np.column_stack([form_u, np.log(np.clip(market, 1e-4, 1))])


def fit_combined(samples, beta):
    u, starts = form_scores(samples, beta)
    market = np.concatenate([s[3] for s in samples])
    _, _, won = _pack(samples)
    return fit(combined_design(u, market), starts, won)
