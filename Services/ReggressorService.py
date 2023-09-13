import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import holidays as hd
import joblib as job
import bz2 as bz

import warnings
warnings.filterwarnings("ignore")

from logging import Logger

from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingRegressor

from Transfer.GetReggressorPredictionQuery import GetPredictionQuery
from Transfer.ReggressorPredictionDto import ReggressorPredictionDto
from Transfer.CountryCodeDto import CountryCodeDto

from Providers.ReggressorsProvider import ReggressorProvider
from Providers.LoggerProvider import LoggerProvider


_FUTURECOVERMULTIPLER: int = 2
_COLERATIONTHRESHOLD: float = 0.20
_MAXIMUMLAGCOUNT: int = 168
_TESTSIZE: float = 0.3


class ReggressorService:
    _dataFrame: pd.DataFrame = None
    _regressor: VotingRegressor = None

    _regressorProvider: ReggressorProvider = ReggressorProvider()
    _logger: Logger = LoggerProvider().GetLogger()

    def GetReggressonModel(self, columnId: int, lag: int) -> VotingRegressor:
        regressor: VotingRegressor = self._regressorProvider.GetVotingRegressor()

        dataFrame: pd.DataFrame = pd.read_csv(r"Assets/train_data.csv")

        dataFrame.columns = [str(i) for i in range(len(dataFrame.columns))]

        dataFrame.rename(columns={"0": "index"}, inplace=True)       

        dataFrame = pd.DataFrame(
            {
                "index": dataFrame["index"],
                str(columnId): dataFrame[str(columnId)],
            }
        )

        dataFrame["index"] = pd.to_datetime(dataFrame["index"])

        dataFrame = dataFrame.set_index("index").sort_index()

        #dataFrame.index = dataFrame.index.tz_localize("UTC")

        self._AddLagFeature(dataFrame, lag, str(columnId))

        self._AddTimeFeature(dataFrame, CountryCodeDto(code="PT"))

        revelantDataFrame, _ = self._GetRevelantDataFrame(dataFrame, columnId)

        train, _ = train_test_split(revelantDataFrame, test_size=_TESTSIZE, shuffle=True)

        X_train = train.drop(str(columnId), axis=1)
        y_train = train[str(columnId)]

        regressor.fit(X_train, y_train)

        return regressor
    
    def GetReggresorPrediciton(
        self, query: GetPredictionQuery
    ) -> ReggressorPredictionDto:
        self._SetDataFrame(query)

        _revelantDataFrame, _ = self._GetRevelantDataFrame(self._dataFrame,query.timeSeriesDictId)

        _futureIndex: pd.DatetimeIndex = pd.date_range(
            self._dataFrame.index[-1], periods=query.predictionTicks + 1, freq="H"
        )[1:]

        _futureDataFrame: pd.DataFrame = pd.DataFrame(
            index=_futureIndex, columns=self._dataFrame.columns
        )

        _futureDataFrame = pd.concat(
            [
                self._dataFrame.tail(query.predictionTicks * _FUTURECOVERMULTIPLER),
                _futureDataFrame,
            ]
        )

        self._AddLagFeature(
            _futureDataFrame,
            query.predictionTicks,
            str(query.timeSeriesDictId),
            dropNaN=False,
        )

        self._AddTimeFeature(_futureDataFrame, query.countryCode)

        if(os.path.exists(f"Assets/Models/{query.timeSeriesDictId}/{query.predictionTicks}.joblib")):
            with bz.open(f"Assets/Models/{query.timeSeriesDictId}/{query.predictionTicks}.joblib", "rb") as file:
                self._regressor = job.load(file)
        else:
            self._SetReggressor(_revelantDataFrame, query.timeSeriesDictId)

        regressorColums: list[str] = self._regressor.feature_names_in_

        _futureDataFrame = _futureDataFrame[regressorColums]

        _futureDataFrame.dropna(inplace=True)

        _prediction: np.ndarray = self._regressor.predict(_futureDataFrame)

        _predictionTimeSeries: dict[str, float] = {
            str(key): float(value)
            for key, value in dict(zip(_futureIndex, _prediction)).items()
        }

        return ReggressorPredictionDto(predictions = _predictionTimeSeries)

    def _GetRevelantDataFrame(
        self, dataFrame: pd.DataFrame,
        timeSeriesId: int
    ) -> tuple[pd.DataFrame, list[str]]:
        colerationSeries: pd.Series = abs(dataFrame.corr()[str(timeSeriesId)])

        colerationIndexes: list = colerationSeries[
            colerationSeries >= _COLERATIONTHRESHOLD
        ].index.tolist()

        return dataFrame[colerationIndexes], colerationIndexes

    def _SetDataFrame(self, query: GetPredictionQuery) -> None:
        self._dataFrame = pd.DataFrame(
            {
                "index": query.timeSeriesDict.keys(),
                str(query.timeSeriesDictId): query.timeSeriesDict.values(),
            }
        )

        self._dataFrame["index"] = pd.to_datetime(self._dataFrame["index"])

        self._dataFrame = self._dataFrame.set_index("index").sort_index()

        #self._dataFrame.index = self._dataFrame.index.tz_localize("UTC")

        self._AddLagFeature(
            self._dataFrame, query.predictionTicks, str(query.timeSeriesDictId)
        )

        self._AddTimeFeature(self._dataFrame, query.countryCode)

        return None

    def _SetReggressor(
        self, learningDataFrame: pd.DataFrame, timeSeriesId: int
    ) -> None:
        train, _ = train_test_split(
            learningDataFrame, test_size=_TESTSIZE, shuffle=True
        )

        X_train = train.drop(str(timeSeriesId), axis=1)
        y_train = train[str(timeSeriesId)]

        self._regressor = self._regressorProvider.GetVotingRegressor()

        self._regressor.fit(X_train, y_train)

        return None

    def _AddLagFeature(
        self,
        dataFrame: pd.DataFrame,
        lagLenght: int,
        timeSeriesId: int,
        dropNaN: bool = True,
    ) -> None:
        maximumLag: int = 0

        for lag in range(lagLenght, 0, -1):
            maximumLag += 1

            if maximumLag > _MAXIMUMLAGCOUNT and dropNaN:
                dataFrame.dropna(inplace=True)
                return None

            dataFrame[f"LAG|{lag}|"] = dataFrame[timeSeriesId].shift(lag + 4)
        if dropNaN:
            dataFrame.dropna(inplace=True)

        return None

    def _AddTimeFeature(self, dataFrame: pd.DataFrame, country: CountryCodeDto) -> None:
        if country.code not in hd.utils.list_supported_countries().keys():
            self._logger.warning(f"Country code {country.code} not supported")
            return None

        countryHoliday: hd.HolidayBase = hd.CountryHoliday(country.code)

        dataFrame["h"] = dataFrame.index.hour
        dataFrame["w"] = dataFrame.index.weekday
        dataFrame["d"] = dataFrame.index.day
        dataFrame["m"] = dataFrame.index.month
        dataFrame["y"] = dataFrame.index.year

        dataFrame["s"] = dataFrame["m"].apply(
            lambda x: 1
            if x in [12, 1, 2]
            else 2
            if x in [3, 4, 5]
            else 3
            if x in [6, 7, 8]
            else 4
        )

        dataFrame["hd"] = dataFrame.index.isin(countryHoliday)

        dataFrame["hd"] = dataFrame["hd"].apply(lambda x: 1 if x == True else 0)

        return None
