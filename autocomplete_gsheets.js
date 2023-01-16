// Put into Google Sheets -> Extensions -> Apps Script -> Code.gs
// Edit Triggers so for the spreadsheet changes - On change

// Date range for google sheet sorting
SORT_DATA_RANGE = "A2:N999"; 

// Sort by Criovial information, Date, and Growth Days 
// 1 = column number, sort by ascending order 
SORT_ORDER = [
{column: 1, ascending: true}, 
{column: 2, ascending: true},
{column: 3, ascending: true}
];

// Function runs when there's an edit in google sheets
function onEdit(e){
  multiSortColumns();
}

// Sort Table by data range and order
function multiSortColumns(){
  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getRange(SORT_DATA_RANGE);
  range.sort(SORT_ORDER);
}

// Logic that needs to be fulfilled 
function extendformula(){
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Set formula for the entire column
  sheet.getRange("C2").setFormula('=ARRAYFORMULA(IF(OR(ISNUMBER(B2)=FALSE,A1<>A2,B2=B1),"",B2-B1))')
  sheet.getRange("H2").setFormula('=ARRAYFORMULA(IF(OR(ISNUMBER(F2)=FALSE,ISNUMBER(G2)=FALSE),"",F2*G2))')
  sheet.getRange("K2").setFormula('=ARRAYFORMULA(IF(OR(ISNUMBER(I2)=FALSE,ISNUMBER(J2)=FALSE),"",I2*J2))')
  sheet.getRange("L2").setFormula('=ARRAYFORMULA(IF(OR(K1="",H2="",C2="",A1<>A2,K1="Final total cells (x10^6)"),"",(H2/K1)/C2))')

  // Sort row based on formula
  var lr = sheet.getLastRow()
  sheet.getRange("C2").copyTo(sheet.getRange(2,3,lr-1))
  sheet.getRange("H2").copyTo(sheet.getRange(2,8,lr-1))
  sheet.getRange("K2").copyTo(sheet.getRange(2,11,lr-1))
  sheet.getRange("L2").copyTo(sheet.getRange(2,12,lr-1))
}

