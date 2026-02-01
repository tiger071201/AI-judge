"""
Demo Script - AI Judge Edge Cases
Demonstrates how the AI Judge handles various challenging inputs
"""

from ai_judge import AIJudge


def demonstrate_edge_cases():
    """Run through various edge cases to show AI Judge capabilities"""
    
    print("="*70)
    print("AI JUDGE DEMONSTRATION - Edge Cases & Robust Handling")
    print("="*70)
    
    judge = AIJudge()
    
    edge_cases = [
        # Category: Normal moves
        ("Normal Moves", [
            ("rock", "Standard move"),
            ("paper", "Standard move"),
            ("scissors", "Standard move"),
        ]),
        
        # Category: Variations
        ("Variations & Misspellings", [
            ("I choose rock", "Natural language"),
            ("let's go with scissors!", "Conversational"),
            ("scisorz", "Misspelling"),
            ("PAPER", "All caps"),
            ("  rock  ", "Extra whitespace"),
        ]),
        
        # Category: Emojis
        ("Emoji Support", [
            ("🪨", "Rock emoji"),
            ("📄", "Paper emoji"),
            ("✂️", "Scissors emoji"),
            ("💣", "Bomb emoji"),
        ]),
        
        # Category: Ambiguous/Unclear
        ("Ambiguous & Unclear Inputs", [
            ("giraffe", "Nonsensical word"),
            ("maybe rock or paper", "Indecisive"),
            ("I don't know", "Unclear intent"),
            ("rock or scissors?", "Multiple options"),
            ("", "Empty input"),
        ]),
        
        # Category: Bomb mechanics
        ("Bomb Constraint", [
            ("bomb", "First bomb use - should be VALID"),
            ("rock", "Normal move after bomb"),
            ("bomb", "Second bomb use - should be INVALID"),
        ]),
    ]
    
    for category, cases in edge_cases:
        print(f"\n{'='*70}")
        print(f"TESTING: {category}")
        print(f"{'='*70}\n")
        
        for user_input, description in cases:
            print(f"Input: '{user_input}' ({description})")
            response = judge.play_round(user_input)
            print(response)
            print("-" * 70)
    
    # Show final result
    print(judge.get_final_result())
    
    # Show detailed history
    print("\n" + "="*70)
    print("GAME HISTORY")
    print("="*70)
    for record in judge.game_state.game_history:
        judgment = record['judgment']
        print(f"\nRound {record['round']}: '{record['user_input'][:40]}'")
        print(f"  Parsed as: {judgment['user_move_parsed']} ({judgment['user_move_status']})")
        print(f"  Bot played: {judgment['bot_move']}")
        print(f"  Winner: {judgment['round_winner']}")
        print(f"  Explanation: {judgment['round_explanation']}")


def demonstrate_prompt_power():
    """Show how prompting drives the logic"""
    
    print("\n" + "="*70)
    print("PROMPT-DRIVEN ARCHITECTURE DEMONSTRATION")
    print("="*70)
    
    judge = AIJudge()
    
    print("\n1. SYSTEM PROMPT")
    print("-" * 70)
    print("The system prompt defines ALL game rules and logic:")
    print(judge.system_prompt[:500] + "...\n")
    
    print("\n2. ROUND PROMPT EXAMPLE")
    print("-" * 70)
    example_round = judge._build_round_prompt("I choose rock")
    print(example_round)
    
    print("\n3. AI JUDGMENT PROCESS")
    print("-" * 70)
    print("For input 'I choose rock', the AI Judge:")
    print("  Step 1: Parses intent → 'rock'")
    print("  Step 2: Validates constraints → VALID (bomb available)")
    print("  Step 3: Applies game logic → Determines winner")
    print("  Step 4: Generates explanation → Clear feedback")
    
    result = judge.judge_move("I choose rock")
    print(f"\nActual AI Response:")
    print(f"  Parsed: {result['user_move_parsed']}")
    print(f"  Status: {result['user_move_status']}")
    print(f"  Explanation: {result['user_move_explanation']}")
    print(f"  Bot Move: {result['bot_move']}")
    print(f"  Winner: {result['round_winner']}")


def show_architecture_diagram():
    """Display the clean architecture separation"""
    
    print("\n" + "="*70)
    print("ARCHITECTURE: SEPARATION OF CONCERNS")
    print("="*70)
    
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│                     "I choose rock"                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              1. INTENT UNDERSTANDING                            │
│              Powered by: Prompt Guidelines                      │
│              Function: _parse_user_move()                       │
│              Output: "rock" (VALID)                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              2. VALIDATION                                      │
│              Powered by: Prompt Constraints                     │
│              Function: _simulate_ai_judgment()                  │
│              Check: Bomb usage, game rules                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              3. GAME LOGIC                                      │
│              Powered by: Prompt Rules                           │
│              Function: _determine_winner()                      │
│              Output: Winner determination                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              4. RESPONSE GENERATION                             │
│              Powered by: Prompt Output Format                   │
│              Function: _format_round_response()                 │
│              Output: Structured feedback to user                │
└─────────────────────────────────────────────────────────────────┘

KEY PRINCIPLE: Prompts define WHAT to do, Code handles HOW to execute
    """)


if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_edge_cases()
    print("\n\n")
    demonstrate_prompt_power()
    print("\n\n")
    show_architecture_diagram()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKey Takeaways:")
    print("✓ AI Judge handles normal moves, variations, and edge cases")
    print("✓ Prompting drives all decision-making logic")
    print("✓ Clean separation between Intent → Validation → Logic → Response")
    print("✓ Explainable decisions with clear reasoning")
    print("✓ Robust constraint enforcement (bomb usage)")
    print("="*70 + "\n")
