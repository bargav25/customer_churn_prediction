from scipy.stats import uniform, randint

LIGHTGBM_PARAMS = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(2, 10),
    'learning_rate': uniform(0.01, 0.1),
    'num_leaves': randint(20, 50),
    'boosting_type': ['gbdt', 'dart', 'goss'],
}

SEARCH_PARAMS = {
    'n_iter': 10,
    'scoring': 'accuracy',
    'cv': 3,
    'verbose': 2,
    'n_jobs': -1,
    'random_state': 42,
}


