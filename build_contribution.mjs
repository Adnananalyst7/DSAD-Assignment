import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Contribution");
sheet.showGridLines = false;

sheet.getRange("A1:C1").merge();
sheet.getRange("A1").values = [["G003 Contribution Sheet"]];
sheet.getRange("A1").format = {
  font: { bold: true, size: 16, color: "#0B2545" },
  horizontalAlignment: "center",
};

sheet.getRange("A3:C3").values = [["Student Registration Number", "Name", "Percentage Contribution"]];
sheet.getRange("A3:C3").format = {
  fill: "#E8EEF5",
  font: { bold: true, color: "#0B2545" },
  borders: { preset: "all", style: "thin", color: "#B8C7D9" },
  wrapText: true,
};

sheet.getRange("A4:C4").values = [["To be filled", "To be filled", 100]];
sheet.getRange("A4:C4").format = {
  borders: { preset: "all", style: "thin", color: "#D9E2EC" },
};
sheet.getRange("C4").format.numberFormat = "0";

sheet.getRange("A6:C6").merge();
sheet.getRange("A6").values = [["Note: Replace the placeholder registration number and name before final submission."]];
sheet.getRange("A6").format = {
  font: { italic: true, color: "#555555" },
  wrapText: true,
};

sheet.getRange("A:A").format.columnWidthPx = 210;
sheet.getRange("B:B").format.columnWidthPx = 210;
sheet.getRange("C:C").format.columnWidthPx = 170;
sheet.getRange("1:6").format.rowHeightPx = 26;

const preview = await workbook.render({ sheetName: "Contribution", autoCrop: "all", scale: 1, format: "png" });
await fs.writeFile("G003_Contribution_preview.png", new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save("G003_Contribution.xlsx");
