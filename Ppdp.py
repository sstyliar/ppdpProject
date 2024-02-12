import json
import copy
from utils import aux_utils
from utils import anonymity_utils
from utils import diversity_utils
from utils import possibility_utils
from utils import information_loss_utils
from utils import generalization_utils
from TaxonomyTree import TaxonomyTree
from Report import Report


class Ppdp:
    def __init__(self, config):
        self.config = config
        self.data = self.populateData()
        self.tTrees = self.getTaxonomyTrees()
        self.hasReport = "report_filename" in self.config and self.config["report_filename"] is not None
        self.reportData = self.getReportData()
        if self.hasReport:
            with open('additionalNotes.txt') as f:
                additionalNotes = f.readlines()
            self.report = Report(self.reportData, self.config["report_filename"], additionalNotes)
            self.report.saveReport()

    def populateData(self):
        # Populate the data prop and create the taxonomy tree
        tmp = {}
        confData = self.config["data"]
        for key in confData:
            rows = aux_utils.readCsvFromConfig(key, self.config)
            tmp[key] = {
                "rows": rows,
                "qi_group": confData[key]["qi_group"],
                "sa_group": confData[key]["sa_group"]
            }
        return tmp

    def getTaxonomyTrees(self):
        ret = {}
        for tableName in self.data:
            if self.config["data"][tableName]["active"]:
                ret[tableName] = TaxonomyTree(self.data[tableName]["rows"], self.config, tableName)
        return ret

    def getReportData(self):
        # Run the generalization logic
        reportData = {"anonymity": {}}
        for tableName in self.data:
            if self.config["data"][tableName]["active"]:
                reportData["anonymity"][tableName] = {
                    "qi_group": self.config["data"][tableName]["qi_group"],
                    "sa_group": self.config["data"][tableName]["sa_group"],
                    "taxonomy_tree": self.tTrees[tableName],
                    "generalization": {}
                }
                for level in range(1, 4):  # 3 levels in total
                    generalizedData = generalization_utils.generalizeTable(copy.deepcopy(self.data[tableName]), self.tTrees[tableName], level, self.config)
                    levelReport = {
                        "k_anonymity": anonymity_utils.getKAnonymity(generalizedData),
                        "l_diversity": diversity_utils.getLDiversity(generalizedData),
                        "entropy_l_diversity": round(float(diversity_utils.getEntropyLDiversity(generalizedData)), 2),
                    }
                    if level > 1:
                        iLoss = information_loss_utils.getILoss(copy.deepcopy(self.data[tableName]), generalizedData, self.config)
                        levelReport["i_loss"] = round(float(iLoss), 2)
                    reportData["anonymity"][tableName]["generalization"][level] = levelReport

        # Find the possibilities
        if self.hasReport:
            reportData["possibilities"] = possibility_utils.getPossibilitiesResults(self.data)

        return reportData


if __name__ == "__main__":
    try:
        with open('config.json', "r") as config_file:
            configuration = json.load(config_file)
            config_file.close()
    except:
        raise Exception("Missing config file")
    Ppdp(configuration)


