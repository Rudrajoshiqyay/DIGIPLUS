# Architecture

This document describes the high-level architecture of the Digiplus project.

## System Workflow

```mermaid
flowchart TD
    Ticket([🎫 Incoming Incident])
    
    Ticket --> Rules[⚡ Rules Engine]
    Ticket --> Similar[🔍 Similar Incidents]
    Ticket --> KB[📚 Knowledge Base]
    
    Rules --> LLM[🤖 LLM / Llama]
    Similar --> LLM
    KB --> LLM
    
    LLM --> Analysis[Evidence-backed Analysis]
    Analysis --> Playbook[Investigation Playbook]
    
    Playbook --> Engineer[👨‍💻 Engineer Decision]
    
    Engineer --> Resolution[Resolution + Feedback]
    Resolution --> History[(Learning History)]
    History -.->|Updates| Similar
```

## Components
1. **Rules Engine**: Deterministic logic for immediate, hardcoded tagging.
2. **Similar Incidents / Learning History**: A vector store (or database) of past resolved tickets used to find historical precedence.
3. **Knowledge Base**: Company documentation, manuals, and standard operating procedures (SOPs).
4. **LLM Engine**: Processes the rule outputs, similar past incidents, and KB articles to generate an evidence-backed analysis and a step-by-step investigation playbook.
5. **Support Engineer**: Reviews the generated playbook and makes the final decision.
6. **Learning History**: A feedback loop where human resolutions are stored back into the database to improve future "Similar Incident" retrieval.
