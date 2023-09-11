import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import pickle as pkl
import bz2 as bz


from sklearn.ensemble import VotingRegressor
from Services.ReggressorService import ReggressorService


class ModelGenerator:
    _reggressorService: ReggressorService = ReggressorService()

    timeStamps: list[str] = [24, 48, 168, 720]

    def GenerateModels(self) -> None:
        tempDataFrame: pd.DataFrame = pd.read_csv(r"Assets/train_data.csv")
        columns: list[str] = tempDataFrame.columns.to_list()

        for column in columns[1:]:
            for ticks in self.timeStamps:
                self.SaveModel(column.replace("cload_", ""), ticks)

    def SaveModel(self, columnId: int, ticks: int) -> None:
        
        if(not os.path.exists(f"Assets/Models/{columnId}")):
            os.mkdir(f"Assets/Models/{columnId}")

        if(not os.path.exists(f"Assets/Models/{columnId}/{ticks}.pkl")):
            with bz.open(f"Assets/Models/{columnId}/{ticks}.pkl", "wb") as file:
                regressor: VotingRegressor = self._reggressorService.GetReggressonModel(columnId, ticks)
                pkl.dump(regressor, file)

ModelGenerator().GenerateModels()
