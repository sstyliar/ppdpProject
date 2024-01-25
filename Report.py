from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from bigtree import hyield_tree


class Report:
    def __init__(self, reportData, config, additionalNotes=None):
        self.reportData = reportData
        self.config = config
        self.additionalNotes = additionalNotes
        self.doc = SimpleDocTemplate(config["report_filename"], pagesize=A4, rightMargin=50, leftMargin=50, topMargin=25, bottomMargin=25)
        self.report = []
        self.styles = getSampleStyleSheet()
        self.buildStyles()
        self.buildReport()
        self.saveReport()

    def buildStyles(self):
        pdfmetrics.registerFont(TTFont('Inconsolata-Medium', "./fonts/Inconsolata-Medium.ttf"))
        self.styles.add(ParagraphStyle("tree_font", fontName="Inconsolata-Medium", fontSize=11))
        self.styles.add(ParagraphStyle("p", fontName="Helvetica", fontSize=12, alignment=0, spaceAfter=10))
        self.styles.add(ParagraphStyle("table_header", fontName="Helvetica-Bold", fontSize=11, alignment=0, spaceAfter=4))
        self.styles.add(ParagraphStyle("header", fontName="Helvetica-Bold", fontSize=16, alignment=0, spaceAfter=15))
        self.styles.add(ParagraphStyle("sub_header", fontName="Helvetica-Bold", fontSize=12, alignment=0, spaceAfter=10))
        self.styles.add(ParagraphStyle("main_title", fontName="Helvetica-Bold", fontSize=18, parent=self.styles["Heading2"], alignment=1, spaceAfter=20))
        self.styles.add(ParagraphStyle("main_sub_title", fontName="Helvetica-Bold", fontSize=16, parent=self.styles["Heading2"], alignment=1, spaceAfter=20))

    def addTable(self, props, headers=None, gridColor=colors.grey, bgColor=colors.aliceblue):
        head = []
        if headers is not None:
            for header in headers:
                head.append(Paragraph(header, self.styles["table_header"]))
            head = [tuple(head)]
        self.report.append(Table(head + props, style=[
            ("GRID", (0, 0), (-1, -1), 1, gridColor),
            ("BACKGROUND", (0, 0), (-1, 0), bgColor),
            ("ROUNDEDCORNERS", [2, 2, 2, 2])
        ]))
        self.report.append(Spacer(1, 10))

    def buildPossibilitiesReport(self):
        self.report.append(Paragraph("Possibilities Report", self.styles["header"]))

        # Possibility of disease with known fields
        self.report.append(Paragraph("For someone with known values what is the possibility of having a specific disease?", self.styles["sub_header"]))
        self.report.append(Paragraph("Known values:", self.styles["p"]))
        self.addTable([["male", "White: British", "70"]], ["Sex", "Race", "Age"])

        self.report.append(Paragraph("The possibilities of someone with the known values to have a specific disease are as follows:", self.styles["p"]))
        props = []
        for disease, possibilities in self.reportData["possibilities"]["disease_possibilities"]:
            props.append((disease, f"{possibilities} %"))
        self.addTable(props, ["Disease", "Possibility"])
        self.report.append(Spacer(1, 10))

        # Direct correlation between hospital and citizens table
        self.report.append(Paragraph("Is there someone on the citizens table that we can be certain of their disease?", self.styles["sub_header"]))
        self.report.append(Paragraph("After querying the hospital able for each citizen the ones that returned only one result are as follows: ", self.styles["p"]))
        props = []
        for name, disease in self.reportData["possibilities"]["certain_diseases"]:
            props.append((name, disease))
        self.addTable(props, ["Name", "Disease"])
        self.report.append(Spacer(1, 20))

    def buildAnonymityPerTableReport(self):
        for tableName in self.reportData["anonymity"]:
            self.report.append(Paragraph(f"Anonymity report for table: {tableName}", self.styles["header"]))
            data = self.reportData["anonymity"][tableName]
            # Groups
            self.addTable([[", ".join(data["qi_group"]), data["sa_group"]]], ["Quasi Identifiers", "Sensitive Attributes"])
            self.report.append(Spacer(1, 10))

            # Generalization
            self.report.append(Paragraph(
                'Anonymity values after the generalization starting from "any" value in the first level and then on with grouping',
                self.styles["sub_header"]))
            generalizationLevels = data["generalization"]
            props = []
            for level in generalizationLevels:
                tmp = [
                    level,
                    generalizationLevels[level]["k_anonymity"],
                    generalizationLevels[level]["l_diversity"],
                    generalizationLevels[level]["entropy_l_diversity"]
                ]
                if "i_loss" in generalizationLevels[level]:
                    tmp.append(generalizationLevels[level]["i_loss"])
                props.append(tmp)
            self.addTable(props, ["Generalization Level", "k Anonymity", "l Diversity", "Entropy l Diversity", "I Loss"])
            self.report.append(Spacer(1, 10))

            # Taxonomy Tree
            self.report.append(Paragraph(f"Taxonomy tree for table: {tableName}", self.styles["header"]))
            tTree = data["taxonomy_tree"].getTree()
            result = hyield_tree(tTree, style="rounded")
            for line in result:
                self.report.append(Paragraph(line.replace(" ", "&nbsp;"), self.styles["tree_font"]))

    def addCustomNotes(self):
        self.report.append(Paragraph("Additional Notes", self.styles["header"]))
        self.report.append(Paragraph("", self.styles["p"]))

    def buildReport(self):
        self.report.append(Paragraph("Privacy Preserving Data Publishing", self.styles["main_title"]))
        self.report.append(Paragraph("Project Report", self.styles["main_sub_title"]))

        # Possibilities
        self.buildPossibilitiesReport()

        # Anonymity per table if needed
        self.buildAnonymityPerTableReport()

    def saveReport(self):
        self.doc.build(self.report)



