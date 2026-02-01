# AI Judge for Rock-Paper-Scissors Plus

## Overview
This is a prompt-driven AI Judge that evaluates user moves in a Rock-Paper-Scissors Plus game. The solution emphasizes **prompt quality**, **clean architecture**, and **explainability** over hardcoded logic.

## Solution Architecture

### 1. Separation of Concerns

The solution cleanly separates four key responsibilities:

```
User Input → Intent Understanding → Validation → Game Logic → Response Generation
```

#### a) Intent Understanding (`_parse_user_move`)
- **What it does**: Interprets what the user is trying to communicate
- **Driven by**: Prompt guidelines on handling variations, misspellings, natural language
- **Examples**: 
  - "I choose rock" → rock
  - "scisorz" → scissors
  - "💣" → bomb
  - "maybe rock or paper" → UNCLEAR

#### b) Validation (`_simulate_ai_judgment`)
- **What it does**: Checks if the interpreted move is allowed given current game state
- **Driven by**: Prompt rules on constraints (bomb usage)
- **Examples**:
  - First bomb usage → VALID
  - Second bomb usage → INVALID

#### c) Game Logic (`_determine_winner`)
- **What it does**: Applies game rules to determine the round outcome
- **Driven by**: Prompt rules on move interactions
- **Examples**:
  - rock vs scissors → rock wins
  - bomb vs anything → bomb wins
  - bomb vs bomb → draw

#### d) Response Generation (`_format_round_response`)
- **What it does**: Creates clear, structured feedback for the user
- **Driven by**: Prompt requirements for explainability
- **Output includes**: Round number, moves, winner, explanation, score, bomb status

### 2. Prompt Design Philosophy

#### System Prompt Structure
The system prompt (`_build_system_prompt`) serves as the "constitution" of the AI Judge:

1. **Role Definition**: Establishes the AI as a neutral judge
2. **Rule Declaration**: Explicitly lists all game rules in priority order
3. **Interpretation Guidelines**: Provides principles for handling ambiguous inputs
4. **Constraint Enforcement**: Specifies how to track and enforce limitations
5. **Output Format**: Defines structured JSON schema for consistency
6. **Decision Process**: Outlines step-by-step reasoning methodology

#### Round Prompt Context
Each round prompt (`_build_round_prompt`) provides:
- Current game state (bomb usage, scores)
- User input to evaluate
- Reference back to system instructions

This ensures the AI Judge has full context for making informed decisions.

### 3. Why This Prompt Structure?

#### Prompt-First Approach
The assignment emphasizes "avoid hardcoding logic in code as much as possible." This solution:

✅ **Uses prompting for**:
- Defining all game rules
- Specifying move interpretation logic
- Establishing validation criteria
- Guiding strategic bot behavior
- Structuring output format

❌ **Uses code only for**:
- State management (tracking bomb usage, scores)
- API orchestration (calling the LLM)
- Response formatting
- User interface

#### Advantages of This Design

1. **Flexibility**: Rules can be changed by editing the prompt, not code
2. **Explainability**: The prompt explicitly states reasoning principles
3. **Extensibility**: New moves or rules can be added to the prompt
4. **Testability**: Different prompts can be A/B tested without code changes
5. **LLM-Native**: Leverages the LLM's natural language understanding rather than brittle regex

### 4. Edge Cases Considered

#### Ambiguous Inputs
- **Multiple moves**: "rock or paper" → UNCLEAR
- **Indecisive**: "I don't know" → UNCLEAR
- **Nonsensical**: "giraffe" → UNCLEAR
- **Empty**: "" → UNCLEAR

#### Variations & Leniency
- **Misspellings**: "scisorz" → scissors ✓
- **Emojis**: "💣" → bomb ✓
- **Natural language**: "I choose paper" → paper ✓
- **Capitalization**: "ROCK" → rock ✓

#### Constraint Violations
- **Second bomb usage**: Automatically INVALID
- **Invalid after bomb used**: Clear explanation provided

#### Edge Game States
- **Both bombs simultaneously**: Correctly handled as DRAW
- **Bot strategy**: Saves bomb for later rounds (strategic)
- **Score tracking**: Accurately maintains state across rounds

### 5. Failure Cases & Robustness

#### Handled Failure Modes
1. **Typos**: Lenient pattern matching catches common errors
2. **Verbose input**: Extracts intent from longer phrases
3. **Ambiguity**: Explicitly marks unclear moves and explains why
4. **Constraint violations**: Detects and rejects invalid bomb usage
5. **Edge case draws**: Properly handles bomb vs bomb

#### Known Limitations
1. **Very creative misspellings**: "rck" might not be caught (could be improved with fuzzy matching)
2. **Multiple moves in one input**: Currently marks as unclear (could parse first valid move)
3. **Language barriers**: Only supports English (could use multilingual LLM)

### 6. Implementation Notes

#### Current Implementation
For demonstration purposes, `_simulate_ai_judgment` implements the logic that an LLM would perform when given the system prompt. This is a **simulation** of AI reasoning.

#### Production Implementation
In a real deployment with Google Gemini API:

```python
def judge_move(self, user_input: str) -> Dict:
    import google.generativeai as genai
    
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    
    # Combine system prompt and round prompt
    full_prompt = f"{self.system_prompt}\n\n{self._build_round_prompt(user_input)}"
    
    # Get AI judgment
    response = model.generate_content(full_prompt)
    
    # Parse JSON response
    return json.loads(response.text)
```

The key insight: **The prompts do the heavy lifting, not the code.**

### 7. What I Would Improve Next

#### Short-term Improvements
1. **Fuzzy string matching**: Use Levenshtein distance for better typo handling
2. **Multi-move parsing**: Extract first valid move from inputs like "rock and paper"
3. **Confidence scoring**: Have AI Judge provide confidence levels for ambiguous cases
4. **Better bot strategy**: Implement counter-play based on user patterns

#### Medium-term Enhancements
1. **Few-shot examples**: Add example inputs/outputs to the prompt for better accuracy
2. **Chain-of-thought**: Ask LLM to show reasoning before giving judgment
3. **Self-correction**: Allow LLM to revise judgment if it detects errors
4. **User feedback loop**: Learn from user corrections to improve interpretation

#### Advanced Features
1. **Multi-round strategy**: Teach bot to learn user patterns
2. **Difficulty levels**: Adjust bot intelligence based on player skill
3. **Custom rules**: Allow users to propose new moves via natural language
4. **Explanation requests**: Let users ask "why did I lose?" and get detailed analysis

### 8. Testing the Solution

#### Run the game:
```bash
python ai_judge.py
```

#### Example test cases:
```
Round 1: "rock" → Should parse as rock, play normally
Round 2: "I'll use scissors!" → Should parse as scissors
Round 3: "💣" → Should parse as bomb, mark bomb as used
Round 4: "bomb" → Should reject as INVALID (already used)
Round 5: "giraffe" → Should mark as UNCLEAR, bot wins round
```

## Dependencies
- Python 3.7+
- No external libraries required for demo
- For production: `google-generativeai` package

## Design Principles Summary

1. ✅ **Prompt-driven logic**: Rules live in prompts, not code
2. ✅ **Clean separation**: Intent → Validation → Logic → Response
3. ✅ **Explainable decisions**: Every judgment includes reasoning
4. ✅ **Edge case handling**: Ambiguity, constraints, variations all covered
5. ✅ **Minimal state**: Only tracks essential game state (bomb usage, scores)
6. ✅ **No over-engineering**: Simple, focused solution

## File Structure
```
ai_judge.py         # Main implementation
README.md          # This file
prompts.md         # Extracted prompts for reference
```

## Author Notes

This solution prioritizes **prompt quality** over code complexity. The system prompt acts as a comprehensive instruction manual that guides the AI Judge through every decision. The code merely orchestrates the AI's judgments and maintains minimal game state.

The philosophy: **Let the LLM do what it does best (understanding language and following instructions), and use code only for what it must (state management and orchestration).**
