import sys
from pdfixsdk import *
from validation import validatePdf
from pdf import autotagPdf, fixUaClauses


def main():
    """
    Main execution function for PDF/UA compliance processing.

    Workflow:
    1. Opens a PDF document
    2. Automatically tags the document for accessibility
    3. Validates against PDF/UA standards
    4. Applies fixes based on validation results
    5. Re-validates the fixed document

    Input/Output Paths:
    - Input: 'pdf/example.pdf' (original document)
    - Intermediate: 'pdf/validate.pdf' (initial validation)
    - Output: 'pdf/tagged.pdf' (final compliant document)

    Exits:
    - Returns 0 on successful completion
    - Returns 1 on error with error message to stderr

    Note:
    Requires PDFix SDK and proper module imports (validation, pdf).
    """
    
    inputPath = "pdf/example.pdf"
    validatePath = "pdf/validate.pdf"
    taggedPath = "pdf/tagged.pdf"

    try:
        pdfix = GetPdfix()
        doc = pdfix.OpenDoc(inputPath, "")
        if not doc:
            raise Exception(GetPdfix().GetError())

        # autotag pdf
        autotagPdf(doc)

        # validate PDF and get failed rules
        rules = validatePdf(doc, validatePath)

        # fix validation results
        fixUaClauses(doc, rules)

        # validate PDF and check final document
        rules = validatePdf(doc, taggedPath)

    except Exception as e:
        print(f"Chyba: {e}", file=sys.stderr)
        sys.exit(1)  # Ukončí skript s chybovým kódom    

    print("All done!")


if __name__ == "__main__":
    main()
