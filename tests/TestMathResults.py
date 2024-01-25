import pytest
from Ppdp import Ppdp


class TestMathResults:
    def __init__(self):
        self.config = {
            "report": None,
            "csv_separator": ";",
            "generalization": {
                "fields": {
                    "race": "str",
                    "age": "int"
                }
            },
            "data": {
                "hospital_data": {
                    "dir": "../tests/data/hospital_data.csv",
                    "active": True,
                    "column_names": ["sex", "race", "age", "disease"],
                    "qi_group": ["race", "age"],
                    "sa_group": "disease"
                }
            }
        }
        self.correctValues = {
            "k_anonymity": [1, 1, 1],
            "l_diversity": [1, 1, 1],
            "entropy_l_diversity": [1, 1, 1],
            "i_loss": [43.01, 22.32],
        }
        self.reportData = Ppdp(self.config).reportData["anonymity"]["hospital_data"]["generalization"]
        self.formatReportData()
        self.assertResults()

    def formatReportData(self):
        # Format report data to match the hardcoded values
        formattedData = {"k_anonymity": [], "l_diversity": [], "entropy_l_diversity": [], "i_loss": []}
        for genLevel in self.reportData:
            if "k_anonymity" in self.reportData[genLevel]:
                formattedData["k_anonymity"].append(self.reportData[genLevel]["k_anonymity"])
            if "l_diversity" in self.reportData[genLevel]:
                formattedData["l_diversity"].append(self.reportData[genLevel]["l_diversity"])
            if "entropy_l_diversity" in self.reportData[genLevel]:
                formattedData["entropy_l_diversity"].append(self.reportData[genLevel]["entropy_l_diversity"])
            if "i_loss" in self.reportData[genLevel]:
                formattedData["i_loss"].append(self.reportData[genLevel]["i_loss"])
        self.reportData = formattedData

    def assertResults(self):
        allG = True
        for metric in self.reportData:
            if metric in self.correctValues:
                try:
                    assert self.reportData[metric] == self.correctValues[metric]
                except:
                    allG = False
                    print(f"{metric} failed assertion for values -> report: {self.reportData[metric]}, correct: {self.correctValues[metric]}")
        if allG:
            print("All tests passed")


if __name__ == "__main__":
    TestMathResults()
