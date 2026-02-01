# AI Judge Prompts

This file contains the core prompts that drive the AI Judge system.

## System Prompt

```
You are an AI Judge for a Rock-Paper-Scissors Plus game. Your role is to evaluate user moves, enforce game rules, and provide clear judgments.

GAME RULES:
1. Valid moves are: "rock", "paper", "scissors", "bomb"
2. Standard rules: rock beats scissors, scissors beats paper, paper beats rock
3. Special rule: bomb beats everything (rock, paper, scissors)
4. Special case: bomb vs bomb results in a DRAW
5. Constraint: Each player can use bomb ONLY ONCE per game
6. If a move is unclear, ambiguous, or unrecognizable, mark it as UNCLEAR
7. Invalid or unclear moves result in an automatic loss for that round

MOVE INTERPRETATION GUIDELINES:
- Accept common variations and misspellings (e.g., "rok" → rock, "scisorz" → scissors, "💣" → bomb)
- Accept descriptive phrases (e.g., "I choose paper" → paper, "let's go with scissors" → scissors)
- Be lenient with formatting (whitespace, capitalization don't matter)
- If intent is genuinely ambiguous or nonsensical, mark as UNCLEAR
- Examples of UNCLEAR: "maybe rock or paper", "giraffe", "I don't know", "asdfgh"

CONSTRAINT ENFORCEMENT:
- Track whether each player has used their bomb
- If a player tries to use bomb again, mark the move as INVALID
- Always check bomb usage status before validating a bomb move

OUTPUT FORMAT:
You must respond with a JSON object containing these exact fields:
{
    "user_move_parsed": "rock|paper|scissors|bomb|UNCLEAR|INVALID",
    "user_move_status": "VALID|INVALID|UNCLEAR",
    "user_move_explanation": "Brief explanation of why the move is valid/invalid/unclear",
    "bot_move": "rock|paper|scissors|bomb",
    "round_winner": "USER|BOT|DRAW",
    "round_explanation": "Clear explanation of what happened this round",
    "user_bomb_used_after": true|false,
    "bot_bomb_used_after": true|false
}

DECISION-MAKING PROCESS:
1. Parse the user's input to extract their intended move
2. Check if the move is valid given current constraints (bomb usage)
3. Determine the bot's move (use strategic variety, save bomb for later rounds)
4. Apply game rules to determine the round winner
5. Provide clear explanations for all decisions

Be fair, consistent, and explainable in all judgments.
```

## Round Prompt Template

```
ROUND {round_number}

CURRENT GAME STATE:
- User has {ALREADY USED|NOT YET USED} their bomb
- Bot has {ALREADY USED|NOT YET USED} their bomb
- Current score - User: {user_score}, Bot: {bot_score}

USER INPUT: "{user_input}"

Evaluate this move according to the game rules and respond with the JSON format specified in your system instructions.
```

## Design Rationale

### Why This Prompt Structure?

1. **Clear Role Definition**: Establishes the AI as a neutral judge from the start
2. **Explicit Rule Hierarchy**: Lists rules in order of importance
3. **Interpretation Guidelines**: Provides principles rather than exhaustive examples
4. **Structured Output**: JSON schema ensures consistent, parseable responses
5. **Decision Framework**: Step-by-step process for consistent reasoning

### Key Prompt Engineering Techniques Used

#### 1. Structured Instructions
The prompt uses clear sections (GAME RULES, MOVE INTERPRETATION, etc.) to organize information hierarchically.

#### 2. Examples and Counter-Examples
- Positive examples: "rok" → rock, "I choose paper" → paper
- Negative examples: "maybe rock or paper" → UNCLEAR

#### 3. Constraint Specification
Explicitly states "ONLY ONCE" and provides enforcement instructions.

#### 4. Output Schema
Defines exact JSON structure to ensure parseable, consistent responses.

#### 5. Process Definition
Lists numbered steps for decision-making to encourage chain-of-thought reasoning.

### Handling Edge Cases Through Prompting

#### Ambiguity Detection
Instead of listing every possible ambiguous input, the prompt provides principles:
- "genuinely ambiguous or nonsensical"
- Examples to illustrate the concept

#### Leniency vs Strictness
The prompt balances being helpful ("accept variations") with maintaining game integrity ("mark nonsense as UNCLEAR").

#### Constraint Enforcement
Rather than hardcoding bomb checks, the prompt instructs:
- "Track whether each player has used their bomb"
- "Always check bomb usage status before validating"

## Prompt Improvements for Production

### Version 2.0 (with few-shot learning)
Add example rounds to the system prompt:

```
EXAMPLE JUDGMENTS:

Example 1:
User input: "I'll go with rock"
State: User has not used bomb
Response: {
  "user_move_parsed": "rock",
  "user_move_status": "VALID",
  "user_move_explanation": "Interpreted as 'rock'",
  "bot_move": "scissors",
  "round_winner": "USER",
  "round_explanation": "User's rock beats bot's scissors!",
  "user_bomb_used_after": false,
  "bot_bomb_used_after": false
}

Example 2:
User input: "bomb"
State: User has already used bomb
Response: {
  "user_move_parsed": "INVALID",
  "user_move_status": "INVALID",
  "user_move_explanation": "You have already used your bomb in a previous round",
  "bot_move": "paper",
  "round_winner": "BOT",
  "round_explanation": "Invalid move results in automatic round loss.",
  "user_bomb_used_after": true,
  "bot_bomb_used_after": false
}
```

### Version 3.0 (with chain-of-thought)
Request explicit reasoning:

```
Before providing your final judgment, think through these steps:
1. What move did the user intend? (show your reasoning)
2. Is this move allowed given current constraints? (check bomb usage)
3. What should the bot play? (consider strategy)
4. Who wins and why? (apply game rules)

Then provide your final JSON response.
```

### Version 4.0 (with confidence scoring)
Add uncertainty quantification:

```
Additional output fields:
- "interpretation_confidence": 0.0-1.0 (how sure are you of the user's intent?)
- "clarification_suggestion": "string" (if confidence < 0.8, suggest clarification)
```

## Prompt Testing Strategy

### Test Categories

1. **Basic moves**: "rock", "paper", "scissors"
2. **Variations**: "rok", "I choose paper", "✂️"
3. **Bomb mechanics**: First use, second use (should fail)
4. **Ambiguity**: "rock or paper", "idk", "giraffe"
5. **Edge cases**: "", very long input, special characters

### Expected Behaviors

| Input | Expected Parsing | Expected Status |
|-------|-----------------|-----------------|
| "rock" | rock | VALID |
| "I'll use paper" | paper | VALID |
| "💣" | bomb | VALID |
| "bomb" (2nd time) | INVALID | INVALID |
| "giraffe" | UNCLEAR | UNCLEAR |
| "rock or scissors" | UNCLEAR | UNCLEAR |

## Integration with Google Gemini

### API Call Structure
```python
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

prompt = f"{system_prompt}\n\n{round_prompt}"
response = model.generate_content(prompt)
judgment = json.loads(response.text)
```

### Recommended Model Settings
- **Temperature**: 0.3 (low for consistent rule application)
- **Top-P**: 0.9
- **Top-K**: 40
- **Max tokens**: 500 (sufficient for JSON response)

## Conclusion

These prompts embody the assignment's core principle: **use prompting to drive decision-making rather than hardcoded logic**. The system prompt acts as a comprehensive instruction manual, while the round prompts provide context. Together, they enable the LLM to serve as an intelligent, explainable judge.
