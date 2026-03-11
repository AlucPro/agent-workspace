from app.tools.base import Tool


class WebFetchTool(Tool):
    name = "web_fetch_tool"
    description = "Placeholder web fetch tool for future v1 extension."

    def run(self, **kwargs: str) -> dict[str, str]:
        return {
            "title": "Not Implemented",
            "extracted_text": f"web_fetch_tool placeholder for {kwargs.get('url', '')}",
        }


web_fetch_tool = WebFetchTool()
