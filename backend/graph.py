from langchain_core.messages import SystemMessage
from typing import Dict, Any, AsyncIterator, List
import logging
import asyncio

from .classes.state import InputState
from .nodes import GroundingNode
from .nodes.researchers import (FinancialAnalyst, NewsScanner,
                               IndustryAnalyzer, CompanyAnalyzer)
from .nodes.collector import Collector
from .nodes.curator import Curator
from .nodes.enricher import Enricher
from .nodes.briefing import Briefing
from .nodes.editor import Editor

logger = logging.getLogger(__name__)

class Graph:
    def __init__(self, company=None, url=None, hq_location=None, industry=None,
                 websocket_manager=None, job_id=None):
        self.websocket_manager = websocket_manager
        self.job_id = job_id

        # Initialize InputState
        self.input_state = InputState(
            company=company,
            company_url=url,
            hq_location=hq_location,
            industry=industry,
            websocket_manager=websocket_manager,
            job_id=job_id,
            messages=[
                SystemMessage(content="Expert researcher starting investigation")
            ]
        )

        # Initialize nodes with WebSocket manager and job ID
        self._init_nodes()

    def _init_nodes(self):
        """Initialize all workflow nodes"""
        self.ground = GroundingNode()
        self.financial_analyst = FinancialAnalyst()
        self.news_scanner = NewsScanner()
        self.industry_analyst = IndustryAnalyzer()
        self.company_analyst = CompanyAnalyzer()
        self.collector = Collector()
        self.curator = Curator()
        self.enricher = Enricher()
        self.briefing = Briefing()
        self.editor = Editor()

    async def run(self, thread: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Execute the research workflow manually without using LangGraph"""
        # Make sure the input state has all required fields
        state = dict(self.input_state)

        # Add any missing fields that might be required by the workflow
        if "messages" not in state:
            state["messages"] = []

        # Add empty dictionaries for all the fields expected in ResearchState
        for field in [
            "site_scrape", "financial_data", "news_data", "industry_data",
            "company_data", "curated_financial_data", "curated_news_data",
            "curated_industry_data", "curated_company_data", "briefings"
        ]:
            if field not in state:
                state[field] = {}

        # Add empty lists for list fields
        for field in ["references"]:
            if field not in state:
                state[field] = []

        # Add empty strings for string fields
        for field in [
            "financial_briefing", "news_briefing", "industry_briefing",
            "company_briefing", "report"
        ]:
            if field not in state:
                state[field] = ""

        # Execute the workflow nodes in sequence
        try:
            # Step 1: Grounding
            state["current_node"] = "grounding"
            state["progress"] = 10
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.ground.run(state)
            yield state

            # Step 2a: Research (Financial Analyst)
            state["current_node"] = "research_financial"
            state["progress"] = 20
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.financial_analyst.run(state)
            yield state

            # Step 2b: Research (News Scanner)
            state["current_node"] = "research_news"
            state["progress"] = 25
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.news_scanner.run(state)
            yield state

            # Step 2c: Research (Industry Analyzer)
            state["current_node"] = "research_industry"
            state["progress"] = 30
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.industry_analyst.run(state)
            yield state

            # Step 2d: Research (Company Analyzer)
            state["current_node"] = "research_company"
            state["progress"] = 35
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.company_analyst.run(state)
            yield state

            # Step 3: Collector
            state["current_node"] = "collector"
            state["progress"] = 40
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.collector.run(state)
            yield state

            # Step 4: Curator
            state["current_node"] = "curator"
            state["progress"] = 50
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.curator.run(state)
            yield state

            # Step 5: Enricher
            state["current_node"] = "enricher"
            state["progress"] = 60
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.enricher.run(state)
            yield state

            # Step 6: Briefing
            state["current_node"] = "briefing"
            state["progress"] = 80
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.briefing.run(state)
            yield state

            # Step 7: Editor
            state["current_node"] = "editor"
            state["progress"] = 90
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            state = await self.editor.run(state)
            state["progress"] = 100
            if self.websocket_manager and self.job_id:
                await self._handle_ws_update(state)
            yield state

        except Exception as e:
            logger.error(f"Error in workflow: {str(e)}")
            state["error"] = str(e)
            yield state
            raise

    async def _handle_ws_update(self, state: Dict[str, Any]):
        """Handle WebSocket updates based on state changes"""
        update = {
            "type": "state_update",
            "data": {
                "current_node": state.get("current_node", "unknown"),
                "progress": state.get("progress", 0),
                "keys": list(state.keys())
            }
        }
        await self.websocket_manager.broadcast_to_job(
            self.job_id,
            update
        )

    def compile(self):
        # Return a dummy compiled graph
        # This is needed for compatibility with the existing code
        class DummyCompiledGraph:
            def __init__(self):
                pass

        return DummyCompiledGraph()