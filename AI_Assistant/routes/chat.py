import asyncio
import json
from pathlib import Path
from typing import AsyncIterator
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    message_to_dict,
    messages_from_dict,
)
from openai import APIError, RateLimitError
from AI_Assistant.utils.schemas import ChatRequest, ChatResponse
from AI_Assistant.core.agent import State_graph
from AI_Assistant.core.prompts import SYSTEM_PROMPT
from AI_Assistant.utils.logger import get_logger



router = APIRouter()
graph = State_graph()
logger = get_logger(__name__)

cache_path = Path(__file__).resolve().parents[2] /"logs"/ "cache.json"
chat_locks: dict[str, asyncio.Lock] = {}
cache_write_lock = asyncio.Lock()


def _new_state() -> dict:
    return {
        "messages": [SystemMessage(content=SYSTEM_PROMPT)],
        "plans": [],
    }


def _load_chat_states() -> dict[str, dict]:
    if not cache_path.exists():
        return {}

    try:
        saved_chats = json.loads(cache_path.read_text(encoding="utf-8"))
        return {
            chat_id: {
                "messages": messages_from_dict(saved_state["messages"]),
                "plans": saved_state.get("plans", []),
            }
            for chat_id, saved_state in saved_chats.items()
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        logger.warning(
            "Unable to restore chat cache; starting with empty state",
            extra={"event": "cache_load_failed", "cache_path": str(cache_path)},
            exc_info=True,
        )
        return {}


def _cache_snapshot() -> dict[str, dict]:
    return {
        chat_id: {
            "messages": [message_to_dict(message) for message in state["messages"]],
            "plans": state.get("plans", []),
        }
        for chat_id, state in chat_states.items()
    }


def _overwrite_cache(snapshot: dict[str, dict]) -> None:
    temporary_path = cache_path.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary_path.replace(cache_path)


async def _save_chat_states() -> None:
    snapshot = _cache_snapshot()
    try:
        async with cache_write_lock:
            await asyncio.to_thread(_overwrite_cache, snapshot)
    except OSError:
        logger.error(
            "Unable to save chat cache",
            extra={"event": "cache_save_failed", "cache_path": str(cache_path)},
            exc_info=True,
        )


chat_states: dict[str, dict] = _load_chat_states()


async def _run_agent_steps(request: ChatRequest) -> AsyncIterator[dict]:
    """Run one chat turn and yield its planning and final-output events."""
    chat_id = request.chat_id or str(uuid4())
    lock = chat_locks.setdefault(chat_id, asyncio.Lock())

    async with lock:
        state = chat_states.setdefault(chat_id, _new_state())
        state["messages"].append(HumanMessage(content=request.message))
        await _save_chat_states()
        yield {"event": "chat_started", "chat_id": chat_id}

        for _ in range(10):
            try:
                state = await graph.ainvoke(state)
            except RateLimitError:
                logger.warning(
                    "LLM provider rate limit reached",
                    extra={"event": "llm_rate_limit", "chat_id": chat_id},
                    exc_info=True,
                )
                yield {
                    "event": "error",
                    "status": 429,
                    "detail": "The AI provider is temporarily rate-limited. Please retry shortly.",
                }
                return
            except APIError:
                logger.error(
                    "LLM provider request failed",
                    extra={"event": "llm_api_error", "chat_id": chat_id},
                    exc_info=True,
                )
                yield {
                    "event": "error",
                    "status": 502,
                    "detail": "The AI provider could not process the request.",
                }
                return

            chat_states[chat_id] = state
            await _save_chat_states()
            response = state["structured_response"]

            if response.step == "OUTPUT":
                logger.info(
                    "Agent answer generated",
                    extra={"event": "agent_output", "chat_id": chat_id},
                )
                yield {"event": "output", "chat_id": chat_id, "response": response.content}
                return

            if response.step == "PLAN":
                logger.info(
                    "Agent planning step",
                    extra={"event": "agent_plan", "chat_id": chat_id},
                )
                yield {"event": "plan", "chat_id": chat_id, "content": response.content}
                state["messages"].append(
                    HumanMessage(content="Continue from your plan. Return step='OUTPUT' when ready.")
                )
                await _save_chat_states()
                continue

            yield {
                "event": "error",
                "status": 501,
                "detail": f"Agent step '{response.step}' is not implemented yet.",
            }
            return

        yield {
            "event": "error",
            "status": 500,
            "detail": "Agent exceeded the maximum number of planning steps.",
        }


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    async def event_stream() -> AsyncIterator[str]:
        async for event in _run_agent_steps(request):
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    chat_id = request.chat_id or str(uuid4())
    lock = chat_locks.setdefault(chat_id, asyncio.Lock())

    # Preserve message order if a client sends two requests for one chat at once.
    async with lock:
        state = chat_states.setdefault(chat_id, _new_state())
        logger.info(
            "Chat message received",
            extra={
                "event": "chat_message",
                "chat_id": chat_id,
                "user_message": request.message,
            },
        )
        state["messages"].append(HumanMessage(content=request.message))
        await _save_chat_states()

        # The graph emits planning steps before its final OUTPUT step.
        for _ in range(10):
            try:
                state = await graph.ainvoke(state)
            except RateLimitError as exc:
                logger.warning(
                    "LLM provider rate limit reached",
                    extra={"event": "llm_rate_limit", "chat_id": chat_id},
                    exc_info=True,
                )
                raise HTTPException(
                    status_code=429,
                    detail="The AI provider is temporarily rate-limited. Please retry shortly.",
                ) from exc
            except APIError as exc:
                logger.error(
                    "LLM provider request failed",
                    extra={"event": "llm_api_error", "chat_id": chat_id},
                    exc_info=True,
                )
                raise HTTPException(
                    status_code=502,
                    detail="The AI provider could not process the request.",
                ) from exc
            chat_states[chat_id] = state
            await _save_chat_states()
            response = state["structured_response"]

            if response.step == "OUTPUT":
                chat_states[chat_id] = state
                logger.info(
                    "Agent answer generated",
                    extra={
                        "event": "agent_output",
                        "chat_id": chat_id,
                        "response": response.content,
                    },
                )
                return ChatResponse(
                    chat_id=chat_id,
                    response=response.content,
                )

            if response.step == "PLAN":
                logger.info(
                    "Agent planning step",
                    extra={
                        "event": "agent_plan",
                        "chat_id": chat_id,
                        "plan": response.content,
                    },
                )
                state["messages"].append(
                    HumanMessage(
                        content="Continue from your plan. Return step='OUTPUT' when ready."
                    )
                )
                await _save_chat_states()
                continue

            logger.warning(
                "Agent step is not implemented",
                extra={"event": "unsupported_step", "chat_id": chat_id, "step": response.step},
            )
            raise HTTPException(
                status_code=501,
                detail=f"Agent step '{response.step}' is not implemented yet.",
            )

        logger.error(
            "Agent exceeded the maximum planning steps",
            extra={"event": "planning_limit_reached", "chat_id": chat_id},
        )
        raise HTTPException(
            status_code=500,
            detail="Agent exceeded the maximum number of planning steps.",
        )
