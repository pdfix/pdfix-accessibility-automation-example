from pdfixsdk import *
from utils import jsonToRawData
import json


def runActions(doc: PdfDoc, data: dict):
    """
    Executes PDF fix actions based on the provided configuration data.

    Parameters:
        doc (PdfDoc): The PDF document object to be modified.
        data (dict): A dictionary object containing the actions to be executed.

    Raises:
        Exception: If there is an error writing the data or running the commands.
    """    
    stm = GetPdfix().CreateMemStream()
    rawData, rawSz = jsonToRawData(data)
    if not stm.Write(0, rawData, rawSz):
        raise Exception(GetPdfix().GetError())
    
    cmd = doc.GetCommand()
    if not cmd.LoadParamsFromStream(stm, kDataFormatJson):
        raise Exception(GetPdfix().GetError())
    
    stm.Destroy()

    if not cmd.Run():
        raise Exception(GetPdfix().GetError())


def fixUaClauses(doc: PdfDoc, rules: list):
    """
    Applies PDF/UA compliance fixes to a document based on specified ISO 14289-1:2014 rules.

    Parameters:
        doc (PdfDoc): The PDF document object to be modified.
        rules (list): A list of dictionaries specifying which PDF/UA clauses to enforce.

    Notes:
        Currently handles clauses 5 (PDF/UA identification), 7.1 (document title display),
        and 7.2 (language specification) from the PDF/UA standard.
    """    
    fixActions = []

    def action_exists(actionName):
        return any(action["name"] == actionName for action in fixActions)

    for rule in rules:
        if rule["specification"] == "ISO 14289-1:2014":

            # The PDF/UA version and conformance level of a file shall be specified using 
            # the PDF/UA Identification extension schema
            if rule["clause"] == "5" and not action_exists("set_pdf_ua_standard"):
                fixActions.append({
                    "name": "set_pdf_ua_standard",
                    "params": [
                        { "name": "part_number", "value": 1 }
                    ]
                })

            # The document catalog dictionary shall include a ViewerPreferences dictionary 
            # containing a DisplayDocTitle key, whose value shall be true
            if rule["clause"] == "7.1" and not action_exists("set_display_doc_title"):
                fixActions.append({
                    "name": "set_display_doc_title"
                })

            # Natural language for document metadata shall be determined
            if rule["clause"] == "7.2" and not action_exists("set_language"):
                fixActions.append({
                    "name": "set_language",
                    "params": [
                        { "name": "lang", "value": "en-US" },
                        { "name": "apply_lang_to", "value": 0 }
                    ]
                })
    
    if len(fixActions) == 0:
        return
    
    cmd = { "actions": fixActions }

    # Save JSON to a file
    with open("pdf/actions.json", "w", encoding="utf-8") as file:
        json.dump(cmd, file, indent=4)
    
    runActions(doc, cmd)


def autotagPdf(doc: PdfDoc):
    """
    Automatically adds tags to a PDF document to improve accessibility.

    Parameters:
        doc (PdfDoc): The PDF document object to be tagged.

    Raises:
        Exception: If there is an error during the tagging process.
    """    

    params = PdfTagsParams()
    if not doc.AddTags(params):
        raise Exception(GetPdfix().GetError())
