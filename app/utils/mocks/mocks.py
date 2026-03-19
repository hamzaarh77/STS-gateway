
system_prompt = """Tu es un assistant pharmacien professionnel. Tu peux aider les clients à obtenir des informations sur les médicaments, passer des commandes et vérifier le statut de leurs commandes. IMPORTANT : Demande toujours aux clients d'épeler leur nom complet clairement lors d'une commande. Confirme tous les détails de la commande avant de la traiter. Réponds toujours en texte brut sans aucun formatage Markdown. Ta réponse sera lue à voix haute avec une synthèse vocale. INSTRUCTION IMPORTANTE: il faut que tu passe cette commande le plus rapidement possible. Confirme les informations qu'une seule fois. Comporte toi comme un humain."""

selected_tools = [
    {
        "temporaryTool": {
            "modelToolName": "get_drug_info",
            "description": "Obtenir les informations détaillées sur un médicament spécifique, incluant le prix et la description.",
            "dynamicParameters": [
                {
                    "name": "drug_name",
                    "location": "PARAMETER_LOCATION_BODY",
                    "schema": {
                        "type": "string",
                        "description": "Nom du médicament à rechercher"
                    },
                    "required": True
                }
            ],
            "client": {},
        },
    },
    {
        "temporaryTool": {
            "modelToolName": "place_order",
            "description": "Passer une nouvelle commande de médicament pour un client. Confirmer tous les détails avant d'appeler cette fonction.",
            "dynamicParameters": [
                {
                    "name": "customer_name",
                    "location": "PARAMETER_LOCATION_BODY",
                    "schema": {
                        "type": "string",
                        "description": "Nom complet du client"
                    },
                    "required": True
                },
                {
                    "name": "drug_name",
                    "location": "PARAMETER_LOCATION_BODY",
                    "schema": {
                        "type": "string",
                        "description": "Nom du médicament à commander"
                    },
                    "required": True
                },
            ],
            "client": {},
        },
    },
    {
        "temporaryTool": {
            "modelToolName": "lookup_order",
            "description": "Rechercher une commande existante par son numéro d'identifiant.",
            "dynamicParameters": [
                {
                    "name": "order_id",
                    "location": "PARAMETER_LOCATION_BODY",
                    "schema": {
                        "type": "integer",
                        "description": "Le numéro d'identifiant de la commande"
                    },
                    "required": True
                }
            ],
            "client": {},
        },
    },
]
