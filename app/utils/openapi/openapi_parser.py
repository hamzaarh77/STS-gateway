from pathlib import Path

from app.dto import ToolIdentifierDTO
from app.entities.tool import Tool
from app.entities.tool import Parameter
from app.services.fileManager.json_file_manager import JsonFileManager

BASE_DOC_PATH = Path(__file__).parent

_json_file_manager = JsonFileManager()
_cached_doc: dict[str, dict] = {}


class OpenApiParser:

    @classmethod
    def _load_spec(cls, domain: str) -> dict:
        if domain not in _cached_doc:
            doc_path = BASE_DOC_PATH / "docs" / f"{domain}.json"
            _cached_doc[domain] = _json_file_manager.read(doc_path)
        return _cached_doc[domain]

    @classmethod
    def _resolve_ref(cls, ref: str, spec: dict) -> dict:
        parts = ref.removeprefix("#/").split("/")

        ref_node = spec
        for part in parts:
            ref_node = ref_node[part]
        return ref_node

    @classmethod
    def _extract_parameters(cls, spec_details: dict, spec: dict) -> list[Parameter]:
        request_body = spec_details.get("requestBody")
        if not request_body:
            return []

        content = request_body.get("content", {})
        request_body_schema = content.get(
            "application/json", {}).get("schema", {})
        if "$ref" in request_body_schema:
            request_body_schema = cls._resolve_ref(
                request_body_schema["$ref"], spec)

        required_fields = request_body_schema.get("required", [])
        return [
            Parameter(
                name=prop_name,
                type=prop_schema.get("type", "string"),
                description=request_body_schema.get(
                    "properties", {})[prop_name],
                required=prop_name in required_fields,
            )
            for prop_name, prop_schema in request_body_schema.get("properties", {}).items()
        ]

    @classmethod
    def get_tool(cls, tool: ToolIdentifierDTO) -> Tool | None:
        spec = cls._load_spec(tool['domain'])

        for path, methods in spec.get("paths", {}).items():
            for method, spec_detail in methods.items():
                if spec_detail.get("operationId") == tool['name']:
                    return Tool(
                        name=tool['name'],
                        description=spec_detail.get("description"),
                        parameters=cls._extract_parameters(spec_detail, spec),
                        http_endpoint=path,
                        http_method=method.upper(),
                    )

        return None
