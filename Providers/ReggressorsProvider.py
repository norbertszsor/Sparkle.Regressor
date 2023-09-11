from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, VotingRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor


class ReggressorProvider:
    _mlpr: MLPRegressor = MLPRegressor(
        hidden_layer_sizes=(50, 50),
        activation="tanh",
        solver="adam",
        alpha=0.01,
        learning_rate="adaptive",
        learning_rate_init=0.01,
        max_iter=1000,
        random_state=42,
        verbose=False,
        early_stopping=True,
        n_iter_no_change=50,
    )

    _xgbr: XGBRegressor = XGBRegressor(
        learning_rate=0.01,
        max_depth=2,
        min_child_weight=10,
        n_estimators=800,
        n_jobs=-1,
        random_state=42,
        verbosity=1,
    )

    _rfr: RandomForestRegressor = RandomForestRegressor(
        n_estimators=300,
        random_state=100,
        max_depth=10,
        min_samples_leaf=1,
        criterion="squared_error",
    )

    _dtr: DecisionTreeRegressor = DecisionTreeRegressor(
        random_state=100, 
        max_depth=10, 
        min_samples_leaf=1, 
        criterion="squared_error"
    )

    _etr: ExtraTreesRegressor = ExtraTreesRegressor(
        n_estimators=300,
        random_state=100,
        max_depth=10,
        min_samples_leaf=1,
        criterion="squared_error",
    )

    vr: VotingRegressor = VotingRegressor(
        estimators=[
            ("MLPRegressor", _mlpr),
            ("XGBRegressor", _xgbr),
            ("RandomForestRegressor", _rfr),
            ("DecisionTreeRegressor", _dtr),
            ("ExtraTreesRegressor", _etr),
        ],
        n_jobs=-1,
    )

    def GetVotingRegressor(self) -> VotingRegressor:
        return self.vr
