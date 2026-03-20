# Lancer le projet projet

``` 
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## client:
`
wscat -c ws://localhost:8000/ws/voice/c084f1a1-bd6a-41bf-b610-cba91128e13f
`

## Lint:
`
autopep8 --in-place --recursive app/ 
`

# Informations sur le projet

## Architecture Projet xVoice

xVoice est un projet voice Agent multi-domaines permettant à des professionnels de déployer un agent vocal intelligent, et de consulter via un back-office les interactions des appels.
Le projet repose sur deux services :

1. **FastAPI (ai-gateway)** — Ce repo. Orchestrateur stateless qui gère les sessions vocales via WebSocket, connecte le client au fournisseur STS (Speech-to-Speech), et exécute les tools métier via le tools-provider.
2. **Laravel (tools-provider)** — Micro-service dédié aux outils métier (commandes, rendez-vous, infos partenaire...). Expose des endpoints utilisés comme tools par l'agent vocal, gère la logique métier et la base de données.

**Fonctionnement :**

1. **Connexion** — Le client se connecte via WebSocket `/ws/voice/{partner_id}`
2. **Contexte** — FastAPI appelle Laravel (`GET /partner-context/{partner_id}`) pour récupérer la config STS (prompt, voix, langue...) et la liste des tools du partenaire
3. **Session vocale** — Deux tâches parallèles : capture micro → envoi au STS provider, et réception STS → lecture audio ou traitement des messages
4. **Appel des tools** — Si l'agent vocal décide d'utiliser un tool, le message handler intercepte la demande, le `ToolCallerService` fait un appel HTTP vers Laravel, et le résultat est renvoyé au STS provider

## Architecture Interne (FastAPI)

**Pattern en couches** : Route → Controller → Services (Entry Point, Facades, Registries)

- La **Route** (`voice.py`) enregistre le WebSocket et délègue au controller
- Le **Controller** (`VoiceController`) assemble les dépendances (STS provider, audio transport, message handler) et lance la session via l'entry point
- Le **VoiceSessionEntryPoint** orchestre la session vocale : connexion STS, lancement parallèle capture/réception
- Les **Facades** (`STSProviderFacade`, `AudioTransportFacade`) exposent un accès simplifié aux registries
- Les **Registries** (`STSProviderRegistry`, `AudioTransportRegistry`) permettent d'enregistrer et résoudre les implémentations par type (pattern Strategy)
- Les **Services** contiennent la logique : `ToolCallerService` (exécution des tools), `StsConfigService` (récupération du contexte partenaire)
- Les **Entities** (`Tool`, `Parameter`) sont des structures de données métier avec comportement
- Les **DTOs** (`StsConfigDTO`, `ToolIdentifierDTO`) sont des conteneurs de données passifs (dataclass)

**Providers (Peuvent évoluer) :**
Notre archi modulaire, permetrai de changer de provider facilement on implémentant juste ce qu'il faut comme logique pour le nouveau.

- **STS** : Ultravox (actuel) Chaque provider a son propre `MessageHandler`
- **Audio Transport** : Local via sounddevice (actuel), ou Twilio, etc.

**Ce que FastAPI ne fait PAS :**
- Pas de base de données, pas de persistance
- Pas de logique métier complexe — tout est délégué à Laravel
- Pas de validation business — c'est le rôle du tools-provider

## Structure du projet

Ici il s'agit d'une structure de base V1, qui sera respecter toute au long de l'évolution du projet.

```
app/
  __init__.py                          # Factory pattern (app_factory)
  controllers/
    voice_controller.py                # Assemblage des dépendances, lance la session
  routes/
    voice.py                           # WebSocket route /ws/voice/{partner_id}
  services/
    voice_session_entry_point.py       # Orchestrateur de la session vocale
    tool_caller_service.py             # Exécution des tools via HTTP vers Laravel
    sts_provider/
      sts_provider.py                  # ABC du provider STS
      sts_provider_registry.py         # Registry des providers
      sts_provider_facade.py           # Facade d'accès au registry
      sts_config_service.py            # Récupération du contexte partenaire
      ultravox/
        ultravox_provider.py           # Implémentation Ultravox
    audio_transport/
      audio_transport.py               # ABC du transport audio
      audio_transport_registry.py      # Registry des transports
      audio_transport_facade.py        # Facade d'accès au registry
      local_audio_transport/
        local_audio_transport.py       # Implémentation locale (sounddevice)
        sound_device_microphone.py     # Capture micro
        sound_device_speaker.py        # Lecture audio
    message_handler/
      base_message_handler.py          # ABC du message handler
      ultravox_message_handler.py      # Handler spécifique Ultravox
    fileManager/
      base_file_manager.py             # ABC lecture/écriture fichiers
      json_file_manager.py             # Implémentation JSON
  entities/
    tool/
      Tool.py                          # Entité Tool (name, description, parameters, endpoint, method)
      Parameter.py                     # Entité Parameter (name, type, description, required)
    order.py                           # Entité Order (legacy/mock)
  dto/
    sts_config_dto.py                  # Config STS du partenaire (prompt, voix, langue, tools...)
    tool_identifier_dto.py             # Référence vers un tool (name + domain)
  enums/
    sts_provider_type.py               # Types de providers STS (ultravox)
    audio_transport_type.py            # Types de transport audio (local, twilio)
    message_handler_types.py           # Types de messages STS
  exceptions/
    invalid_tool_resource_exception.py # Tool introuvable dans le registry
  utils/
    logging_config.py                  # Configuration des logs (rotating file handler)
    openapi/
      openapi_parser.py                # Parsing des specs OpenAPI → entités Tool
      docs/                            # Specs OpenAPI par domaine (copiées depuis Laravel)
        Order.json
        AgentExchanges.json
        PartnerContext.json
  interfaces/
    audio.py                           # Interfaces audio (micro, speaker)
```

## Convention de nommage

| Couche       | Convention fichier         | Convention classe            | Exemple                          |
|--------------|---------------------------|------------------------------|----------------------------------|
| Controller   | `snake_case.py`           | `{Name}Controller`          | `VoiceController`                |
| Route        | `snake_case.py`           | —                            | `voice.py`                       |
| Service      | `snake_case.py`           | `{Name}Service`             | `ToolCallerService`              |
| Entity       | `PascalCase.py`           | `{Name}`                    | `Tool`, `Parameter`              |
| DTO          | `snake_case.py`           | `{Name}DTO`                 | `StsConfigDTO`, `ToolIdentifierDTO` |
| Enum         | `snake_case.py`           | `{Name}Type`                | `STSProviderType`                |
| Exception    | `snake_case.py`           | `{Description}Exception`    | `InvalidToolResourceException`   |
| ABC          | `snake_case.py`           | `{Name}` ou `Base{Name}`   | `STSProvider`, `BaseMessageHandler` |
| Registry     | `snake_case.py`           | `{Name}Registry`            | `STSProviderRegistry`            |
| Facade       | `snake_case.py`           | `{Name}Facade`              | `STSProviderFacade`              |

## OpenAPI & Contrat avec le tools-provider

### Specs OpenAPI

Les specs OpenAPI sont stockées par domaine dans `utils/openapi/docs/` (ex: `Order.json`, `AgentExchanges.json`). Ces fichiers sont copiés depuis le tools-provider Laravel.

### Parsing

`OpenApiParser` parcourt la spec pour transformer un `ToolIdentifierDTO` (name + domain) en entité `Tool` complète :

1. **Chargement** — `_load_spec(domain)` lit le JSON via `JsonFileManager` avec cache par domaine (un fichier lu une seule fois)
2. **Parcours** — Itère sur `paths` → `methods` → cherche le `operationId` correspondant
3. **Extraction des paramètres** — Lit le `requestBody` schema, résout les `$ref`, construit les `Parameter`
4. **Résultat** — Retourne une entité `Tool` avec name, description, parameters, http_endpoint, http_method

### Contrat entre les deux services

**Point d'intégration 1 — Contexte partenaire :**
```
GET /api/partner-context/{partner_id}
→ { data: { stsConfig: {...}, tools: [{name, domain}, ...] } }
```
`StsConfigService` appelle cet endpoint et utilise `OpenApiParser.get_tool()` pour résoudre chaque tool.

**Point d'intégration 2 — Exécution des tools :**
```
{method} /api/{endpoint}
→ { data: {...}, message: "..." }
```
`ToolCallerService` utilise le `http_endpoint` et `http_method` de l'entité `Tool` pour appeler Laravel.

**Clé de liaison :** L'`operationId` OpenAPI (ex: `Order-OrderStore`) sert de nom de tool. Il est identique dans la spec Laravel et dans le `ToolIdentifierDTO` retourné par le partner-context.