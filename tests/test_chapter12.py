import pytest


def test_chapter12_load_digits():
    from chapter12.chapter12_load_digits import data, targets

    assert data[:, 0].size == targets.size


def test_chapter12_fit_predict():
    from chapter12.chapter12_fit_predict import accuracy

    assert accuracy == pytest.approx(0.83, rel=1e-2)


def test_chapter12_pipelines():
    from chapter12.chapter12_pipelines import accuracy

    assert accuracy == pytest.approx(0.83, rel=1e-2)


def test_chapter12_cross_validation():
    from chapter12.chapter12_cross_validation import score

    assert score.mean() == pytest.approx(0.80, rel=1e-2)


def test_chapter12_gaussian_naive_bayes():
    from chapter12.chapter12_gaussian_naive_bayes import model

    assert len(model.theta_[0]) == 64
    assert len(model.sigma_[0]) == 64


def test_chapter12_svm():
    from chapter12.chapter12_svm import score

    assert score.mean() == pytest.approx(0.96, rel=1e-2)


def test_chapter12_finding_parameters():
    from chapter12.chapter12_finding_parameters import grid

    assert grid.best_params_ == {"C": 10, "kernel": "rbf"}
