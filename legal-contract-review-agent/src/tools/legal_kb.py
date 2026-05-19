"""Legal Knowledge Base - provides regulatory checks for clause types."""


class LegalKnowledgeBase:
    def __init__(self):
        self.db = {
            "indemnification": [
                {
                    "id": "GENERAL_INDEMNITY_001",
                    "checks": [
                        {
                            "description": "Indemnity must be mutual between parties",
                            "severity": 5,
                        },
                        {
                            "description": "Cap on liability should be reasonable and proportional",
                            "severity": 3,
                        },
                        {
                            "description": "Indemnity should survive termination",
                            "severity": 2,
                        },
                    ],
                }
            ],
            "payment_terms": [
                {
                    "id": "PAYMENT_STD_001",
                    "checks": [
                        {
                            "description": "Payment period must not exceed 30 days",
                            "severity": 5,
                        },
                        {
                            "description": "Late payment interest rate must be specified and reasonable",
                            "severity": 3,
                        },
                    ],
                }
            ],
            "data_processing": [
                {
                    "id": "GDPR_ART28",
                    "checks": [
                        {
                            "description": "Processing duration must be explicitly stated (GDPR Art.28)",
                            "severity": 5,
                        },
                        {
                            "description": "Nature and purpose of processing must be defined",
                            "severity": 5,
                        },
                        {
                            "description": "Types of personal data must be enumerated",
                            "severity": 4,
                        },
                        {
                            "description": "Processor obligations must be listed",
                            "severity": 3,
                        },
                    ],
                }
            ],
            "termination": [
                {
                    "id": "TERM_STD_001",
                    "checks": [
                        {
                            "description": "Notice period should be reasonable (30-90 days)",
                            "severity": 2,
                        },
                        {
                            "description": "Termination for cause provisions should exist",
                            "severity": 4,
                        },
                    ],
                }
            ],
            "confidentiality": [
                {
                    "id": "CONF_STD_001",
                    "checks": [
                        {
                            "description": "Confidentiality period must be at least 5 years",
                            "severity": 3,
                        },
                        {
                            "description": "Exclusions for public information must be stated",
                            "severity": 2,
                        },
                    ],
                }
            ],
            "liability": [
                {
                    "id": "LIAB_STD_001",
                    "checks": [
                        {
                            "description": "Limitation of liability must exclude gross negligence",
                            "severity": 5,
                        },
                        {
                            "description": "Total liability cap should not be unreasonably low",
                            "severity": 3,
                        },
                    ],
                }
            ],
        }

    def retrieve(self, clause_type: str) -> list:
        return self.db.get(clause_type, [])
