### What is Agentic AI

An autonomous system powered by an LLM
that can perceive its environment, reason
about tasks, and take actions using tools to
achieve specific goals. Unlike standard
chatbots, agents can follow multi-step plans.

```mermaid
graph TD
    subgraph "THE BRAIN (LLM)"
        A[LLM - The Core Engine] 
        B{Reasoning & Planning}
    end

    subgraph "COGNITION"
        C[(Memory)]
        D[Context Window]
    end

    subgraph "PERCEPTION & ACTION"
        E[Tools / Function Calling]
        F[RAG - External Knowledge]
    end

    A --> B
    B <--> C
    B <--> D
    B --> E
    B --> F
    E --> G[External World / APIs]
    F --> H[Vector Database]
```


### important concept around agentic ai

- Prompts
- Tokens
- Content Window
- Tempreture
- RAG
- Function Calling
- MCP
- Agent workflow


### Agentic Pattern

### Agentic workflow Pattern

### RAG Pattern

