---
aliases: []
confidence: 
created: 2025-07-13T06:20:44Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:23Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Independent pizza
type:
uid: 
updated: 
version:
---

For these activities, your new role is to be a curious listener. Resist the urge to guide her. If she says, "I'm stuck," try one of these open-ended questions:

- "What have you tried so far?"
- "Can you draw it out?"
- "What do you notice about the numbers you have so far?"
- "What's the simplest version of the problem you could try?"
  The goal is for her to feel the satisfaction of her own breakthrough.

## Activity 1: The Pizza Topping Puzzle

The Goal: To independently discover a systematic way of counting combinations, a core concept in probability and statistics.

### The Setup

"We're designing a new pizza menu for a restaurant. To keep things simple, customers can choose any combination of toppings they want, but they can only have each topping once. We need to figure out how many different pizzas are possible."

The Independent Challenge:

- Start simple: "If we only have three toppings available – let's say Mushroom (M), Peppers (P), and Onion (O) – how many different pizzas can a customer order? They can have one topping, two toppings, or all three."
- The main puzzle: "Now, what if we have four toppings? Let's add Sweetcorn (S). How many different pizzas are possible now?"

### Your Role

Give her a piece of paper and let her work. She might start by just listing them randomly. Let her. She might miss some or count some twice. That's part of the process. If she's stuck, you could ask, "How could you organise your list to make sure you don't miss any?" or "What if you list all the one-topping pizzas first, then all the two-topping ones?"

### The Deeper Maths (For Your Eyes Only)

She is exploring combinations. For four toppings, she might discover a system:

- 1-topping pizzas: 4 (M, P, O, S)
- 2-topping pizzas: 6 (MP, MO, MS, PO, PS, OS)
- 3-topping pizzas: 4 (MPO, MPS, MOS, POS)
- 4-topping pizzas: 1 (MPOS)
- Total: 4 + 6 + 4 + 1 = 15 different pizzas. (There's also the 16th option: a plain pizza with no toppings!). The pattern of numbers 1, 4, 6, 4, 1 is a row from Pascal's Triangle, a fundamental structure in mathematics. The success here isn't getting the number 15, but in her creating a system to find it.

## Activity 2: The Growing Garden Path

The Goal: To independently discover an algebraic rule (a function) from a visual pattern.

### The Setup

"We're designing a garden path using square paving slabs. The path is always one slab wide. Around the outside of the path, we're going to plant a border of square-metre flowerbeds. We need a rule to figure out how many flowerbeds we need for any length of path."

### The Independent Challenge

Give her some squared paper and a pencil.

- "Can you draw a path that is 1 slab long and show the flowerbeds around it? How many flowerbeds are there?"
- "Now draw a path that is 2 slabs long. How many flowerbeds does it need?"
- "Do the same for a path that is 3 slabs long and 4 slabs long."
- The main puzzle: "Look at your results. Can you find a rule or a formula that would let you predict how many flowerbeds you would need for a path of any length? How many would you need for a path that is 50 slabs long?"
  Your Role:
  The final question is designed to make counting from a drawing impossible, forcing her to look for a pattern. If she's struggling to find the rule, you could ask, "How many flowerbeds are on the top? How many on the bottom? And what about the ends?"
  The Deeper Maths (For Your Eyes Only):
  She will find the number of flowerbeds goes 8, 10, 12, 14...
  There are multiple ways to generate the rule. She might see it as:
- length on top + length on bottom + 2 ends. For a path of length L, this is L + L + 2, which is 2L + 2. (Wait, that's not right... it's L on top, L on bottom, plus 3 at each end... so L+L+6? No, that's not right either. Let me re-think.)
- Let's draw it.
- L=1: 3 on top, 3 on bottom, 2 on sides = 8.
- L=2: 4 on top, 4 on bottom, 2 on sides = 10.
- L=3: 5 on top, 5 on bottom, 2 on sides = 12.
- The number on top is L+2. The number on the bottom is L+2. The two on the sides are always 2. So (L+2) + (L+2) + 2? No, that counts corners twice.
- Let's try another way. The top row has L slabs. The bottom row has L slabs. The two ends have 3 slabs each. So L + L + 3 + 3 = 2L + 6. Let's test it. For L=1, 2(1)+6=8. Correct. For L=2, 2(2)+6=10. Correct. For L=3, 2(3)+6=12. Correct. This is one valid formula.
- Another way: 3 slabs for each slab in the path (3L) but this double-counts.
- Another way: A path of length L has L slabs on top, L slabs on bottom, and one at each end. So L+L+1+1 = 2L+2. Let's test. L=1 -> 4. Incorrect.
- Let's go back to the first drawing. L=1. It's a 3x3 square with the middle missing. So 3x3 - 1 = 8.
- L=2. It's a 4x3 rectangle with the middle two missing. 4x3 - 2 = 10.
- L=3. It's a 5x3 rectangle with the middle three missing. 5x3 - 3 = 12.
- The width of the rectangle is always 3. The length is L+2. The number of missing slabs is L. So the formula is 3(L+2) - L. Let's test it. L=1 -> 3(3)-1=8. Correct. L=2 -> 3(4)-2=10. Correct.
- The beauty is that her formula, whatever it is, is correct as long as it works. The goal is the generative act of finding a rule, not a specific one. For L=50, the answer is 2(50) + 6 = 106.

## Activity 3: The Stable Design Challenge

The Goal: To use geometric reasoning to solve a simple optimisation problem, understanding that sometimes there isn't one "right" answer, but a "best" answer that needs justification.

The Setup:

"You're designing a new stable block for a horse. You have 24 metres of fencing to build a rectangular paddock. You want the horse to have the biggest possible area to run around in."

The Independent Challenge:

"Using exactly 24 metres of fencing for the perimeter, what are all the different rectangular paddocks you could build? Which design gives the horse the most area to live in? The lengths of the sides must be whole numbers."

Your Role:

Give her squared paper. Let her draw different rectangles. She'll need to remember that the perimeter is 2 × (length + width). If she's stuck, you could ask, "If the total perimeter is 24m, what must the length and width add up to?" (Answer: 12m).

The Deeper Maths (For Your Eyes Only):

She is exploring the relationship between perimeter and area. She should discover different possibilities:

- 11m by 1m paddock: Area = 11 m²
- 10m by 2m paddock: Area = 20 m²
- 9m by 3m paddock: Area = 27 m²
- 8m by 4m paddock: Area = 32 m²
- 7m by 5m paddock: Area = 35 m²
- 6m by 6m paddock: Area = 36 m²
  She will independently discover a fundamental mathematical principle: for a fixed perimeter, a square gives the maximum possible area. The success is not just finding the 6x6 paddock, but the process of testing different options and comparing the results to find the optimal solution.
