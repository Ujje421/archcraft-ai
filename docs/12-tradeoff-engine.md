# 12 — Trade-off Engine

> Technology decision engine — structured comparison, recommendation, and challenge.

---

## Overview

The Trade-off Engine helps users make informed technology decisions by:

1. **Comparing** two technologies side-by-side
2. **Recommending** the best technology for a given context
3. **Challenging** existing decisions (argue the opposite side)
4. **Explaining** why a technology was chosen

---

## Comparison Matrix

### Input

```python
@dataclass
class ComparisonRequest:
    tech_a: str                      # "postgresql"
    tech_b: str                      # "dynamodb"
    requirements: list[str]          # Requirements that matter for this system
    context: SystemRequirements      # Full system requirements for weighting
```

### Output

```python
@dataclass
class ComparisonMatrix:
    tech_a: str
    tech_b: str
    criteria: list[ComparisonCriterion]
    recommendation: Recommendation
    
@dataclass
class ComparisonCriterion:
    name: str                        # "Relational data"
    weight: float                    # 0.0 - 1.0 (importance for this system)
    score_a: int                     # 1-5 stars
    score_b: int                     # 1-5 stars
    explanation: str                 # Why these scores

@dataclass
class Recommendation:
    recommended: str                 # "postgresql"
    confidence: float                # 0.0 - 1.0
    reasoning: str                   # "PostgreSQL is preferred because..."
    caveats: list[str]              # "However, at 500K+ writes/sec..."
```

### Example Output

```json
{
  "tech_a": "PostgreSQL",
  "tech_b": "DynamoDB",
  "criteria": [
    {
      "name": "Relational data",
      "weight": 0.9,
      "score_a": 5,
      "score_b": 1,
      "explanation": "PostgreSQL natively supports relations, JOINs, and foreign keys. DynamoDB is a key-value/document store with no native JOIN support."
    },
    {
      "name": "Complex queries",
      "weight": 0.8,
      "score_a": 5,
      "score_b": 2,
      "explanation": "PostgreSQL supports full SQL with aggregations, CTEs, window functions. DynamoDB supports limited query/scan with filter expressions."
    },
    {
      "name": "Massive scale writes",
      "weight": 0.6,
      "score_a": 3,
      "score_b": 5,
      "explanation": "DynamoDB handles millions of writes/sec with auto-scaling. PostgreSQL requires sharding beyond ~50K writes/sec."
    },
    {
      "name": "ACID transactions",
      "weight": 0.7,
      "score_a": 5,
      "score_b": 4,
      "explanation": "PostgreSQL has full ACID. DynamoDB supports transactions across up to 100 items with some limitations."
    },
    {
      "name": "Operational simplicity",
      "weight": 0.4,
      "score_a": 3,
      "score_b": 5,
      "explanation": "DynamoDB is fully managed with zero operational overhead. PostgreSQL requires monitoring, vacuuming, backup management."
    },
    {
      "name": "Flexible schema",
      "weight": 0.3,
      "score_a": 3,
      "score_b": 5,
      "explanation": "DynamoDB is schemaless. PostgreSQL requires schema migrations but supports JSONB for flexible data."
    }
  ],
  "recommendation": {
    "recommended": "PostgreSQL",
    "confidence": 0.82,
    "reasoning": "PostgreSQL is preferred because the system requires relational data modeling, complex queries with JOINs, and strong ACID transactions. The write throughput requirements (17K peak RPS) are well within PostgreSQL's capacity with read replicas.",
    "caveats": [
      "If write throughput exceeds 50K RPS, consider DynamoDB or PostgreSQL with Citus sharding",
      "If operational simplicity is prioritized over query flexibility, DynamoDB becomes more attractive"
    ]
  }
}
```

---

## Scoring Algorithm

```python
class TradeoffEngine:
    
    def compare(self, request: ComparisonRequest) -> ComparisonMatrix:
        # 1. Get component metadata from Knowledge Base
        comp_a = self.kb.get_component(request.tech_a)
        comp_b = self.kb.get_component(request.tech_b)
        
        # 2. Define comparison criteria based on system requirements
        criteria = self._derive_criteria(request.requirements, request.context)
        
        # 3. Score each technology against criteria
        scored_criteria = []
        for criterion in criteria:
            score_a = self._score(comp_a, criterion)
            score_b = self._score(comp_b, criterion)
            weight = self._calculate_weight(criterion, request.context)
            
            scored_criteria.append(ComparisonCriterion(
                name=criterion.name,
                weight=weight,
                score_a=score_a,
                score_b=score_b,
                explanation=self._explain_scores(comp_a, comp_b, criterion),
            ))
        
        # 4. Calculate weighted recommendation
        weighted_a = sum(c.score_a * c.weight for c in scored_criteria)
        weighted_b = sum(c.score_b * c.weight for c in scored_criteria)
        total_weight = sum(c.weight for c in scored_criteria)
        
        recommended = request.tech_a if weighted_a >= weighted_b else request.tech_b
        confidence = abs(weighted_a - weighted_b) / (total_weight * 5)  # Normalize
        
        return ComparisonMatrix(
            tech_a=request.tech_a,
            tech_b=request.tech_b,
            criteria=scored_criteria,
            recommendation=Recommendation(
                recommended=recommended,
                confidence=min(confidence, 1.0),
                reasoning=self._generate_reasoning(comp_a, comp_b, scored_criteria, recommended),
                caveats=self._generate_caveats(comp_a, comp_b, request.context),
            ),
        )
    
    def _score(self, component, criterion) -> int:
        """Score a component against a criterion (1-5).
        
        Uses the component's 'supports' and 'limitations' metadata
        to derive a score. Falls back to knowledge-base lookup tables.
        """
        
        # Check if component explicitly supports this capability
        capability = criterion.capability_key
        
        if capability in component.supports:
            return 5
        elif capability in component.limitations:
            return 1
        else:
            # Lookup from pre-defined scoring tables
            return self.scoring_tables.get(component.slug, {}).get(capability, 3)
```

---

## Pre-defined Scoring Tables

```yaml
# knowledge/scoring_tables.yaml

postgresql:
  relational_data: 5
  complex_queries: 5
  acid_transactions: 5
  horizontal_write_scaling: 3
  horizontal_read_scaling: 4
  operational_simplicity: 3
  flexible_schema: 3
  json_support: 4
  full_text_search: 3
  geospatial: 5
  time_series: 2

dynamodb:
  relational_data: 1
  complex_queries: 2
  acid_transactions: 4
  horizontal_write_scaling: 5
  horizontal_read_scaling: 5
  operational_simplicity: 5
  flexible_schema: 5
  json_support: 5
  full_text_search: 1
  geospatial: 1
  time_series: 2

mongodb:
  relational_data: 2
  complex_queries: 3
  acid_transactions: 4
  horizontal_write_scaling: 4
  horizontal_read_scaling: 4
  operational_simplicity: 4
  flexible_schema: 5
  json_support: 5
  full_text_search: 3
  geospatial: 4
  time_series: 3

kafka:
  high_throughput: 5
  event_replay: 5
  ordering_guarantees: 4
  routing_flexibility: 2
  operational_simplicity: 2
  exactly_once: 4
  multiple_consumers: 5
  low_latency: 3

rabbitmq:
  high_throughput: 3
  event_replay: 1
  ordering_guarantees: 3
  routing_flexibility: 5
  operational_simplicity: 4
  exactly_once: 3
  multiple_consumers: 3
  low_latency: 4
```

---

## Challenge Mode

When the user clicks "Challenge this decision", the AI argues the opposite:

```python
async def challenge(self, technology: str, context: ArchitectureGraph) -> ChallengeResponse:
    """Argue against the current technology choice."""
    
    # Get what technology is being used
    component = self.kb.get_component(technology)
    
    # Find the best alternative
    alternatives = self.kb.get_alternatives(technology)
    best_alt = self._find_best_alternative(alternatives, context)
    
    # Use AI to argue for the alternative
    prompt = f"""
    The architecture currently uses {technology}.
    
    Argue why {best_alt.name} would be a BETTER choice.
    Be specific about:
    1. What problems {technology} will cause
    2. What {best_alt.name} does better
    3. Migration path from {technology} to {best_alt.name}
    4. Counter-arguments (to be fair)
    
    Context: {context.to_json()}
    """
    
    response = await self.ai.generate(prompt)
    
    return ChallengeResponse(
        current=technology,
        challenger=best_alt.name,
        arguments=response.arguments,
        counter_arguments=response.counter_arguments,
        verdict=response.verdict,
    )
```

---

## Architecture Diff Table

Compare two architecture versions:

```python
@dataclass
class ArchitectureDiff:
    version_a: int
    version_b: int
    
    metrics: dict[str, DiffMetric]
    
    added_nodes: list[ArchNode]
    removed_nodes: list[ArchNode]
    changed_nodes: list[NodeChange]
    
    added_connections: list[ArchConnection]
    removed_connections: list[ArchConnection]
    
    explanation: str

@dataclass
class DiffMetric:
    name: str           # "Complexity", "Scalability", etc.
    value_a: str        # "Low"
    value_b: str        # "High"
    direction: str      # "improved", "degraded", "unchanged"
```

Output:

| Category | V1 | V2 | Direction |
|---|---|---|---|
| Complexity | Low | Medium | ↑ Increased |
| Scalability | Low | High | ↑ Improved |
| Availability | Medium | High | ↑ Improved |
| Cost | $ | $$$ | ↑ Increased |
| Operations | Easy | Hard | ↓ Degraded |
| Throughput | Low | High | ↑ Improved |

---

## Related Documents

- [09-component-knowledge-base.md](./09-component-knowledge-base.md) — Component data used for comparison
- [07-ai-engine.md](./07-ai-engine.md) — AI generates challenge arguments
- [02-system-design-schema.md](./02-system-design-schema.md) — Sections 23-24: Trade-offs, Alternatives
