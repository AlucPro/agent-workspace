from typing import Dict, List, Union

from app.schemas.chat import SourceItem
from app.tools.base import Tool


class DocumentLookupTool(Tool):
    name = "document_lookup_tool"
    description = "Returns mock knowledge base chunks for v1 scaffolding."

    def run(self, **kwargs: Union[str, int]) -> Dict[str, List[SourceItem]]:
        query = str(kwargs["query"])
        return {
            "matched_chunks": [
                SourceItem(
                    document_id="doc_v1",
                    file_name="Agent Workspace v1 技术设计文档.md",
                    chunk_id="chunk_01",
                    content=f"命中文档片段（mock）：{query}",
                ),
                SourceItem(
                    document_id="doc_v1",
                    file_name="Agent Workspace v1 技术设计文档.md",
                    chunk_id="chunk_02",
                    content="前端展示内容包括最终回答、intent、sources、tool runs 和 trace。",
                ),
            ]
        }


document_lookup_tool = DocumentLookupTool()
