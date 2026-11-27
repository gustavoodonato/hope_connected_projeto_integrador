from enum import Enum

class TecnologiaImpressoraEnum(str, Enum):
    FDM = "FDM"
    SLA = "SLA"
    SLS = "SLS"
    DLP = "DLP"
    DLMS = "DLMS"
    POLYJET = "PolyJet"
    EBM = "MJF"