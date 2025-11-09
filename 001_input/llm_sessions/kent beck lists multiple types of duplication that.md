---
aliases: []
confidence: 
created: 2025-10-30T14:43:08Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T13:26:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: kent beck lists multiple types of duplication that
type: 
uid: 
updated: 
---

## Kent Beck Lists Multiple Types of Duplication that Need Refactoring Out. List Them and Describe what They Are, and Give Typescript Examples

Kent Beck identifies several types of duplication that need refactoring. Here are the main types along with descriptions and TypeScript examples:

### 1. Duplicated Logic

This occurs when the same expression or logic appears in multiple places in the code[^1_1][^1_2].

Example:

```typescript
function calculateArea(shape: string, width: number, height: number): number {
  if (shape === 'rectangle') {
    return width * height;
  } else if (shape === 'triangle') {
    return (width * height) / 2;
  }
  return 0;
}

function calculatePerimeter(shape: string, width: number, height: number): number {
  if (shape === 'rectangle') {
    return 2 * (width + height);
  } else if (shape === 'triangle') {
    return width + height + Math.sqrt(width**2 + height**2);
  }
  return 0;
}
```

### 2. Data Duplication

This occurs when the same data appears in multiple places, either in code or tests[^1_2].

Example:

```typescript
const TAX_RATE = 0.08;

function calculateTotal(price: number): number {
  return price + (price * 0.08);
}

function estimateTax(price: number): number {
  return price * 0.08;
}
```

### 3. Structural Duplication

This happens when similar code structures are repeated, even if the specific data or operations differ[^1_6].

Example:

```typescript
class Rectangle {
  width: number;
  height: number;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
  }

  area(): number {
    return this.width * this.height;
  }
}

class Circle {
  radius: number;

  constructor(radius: number) {
    this.radius = radius;
  }

  area(): number {
    return Math.PI * this.radius * this.radius;
  }
}
```

### 4. Algorithmic Duplication

This occurs when the same algorithm is implemented in different ways[^1_8].

Example:

```typescript
function sumArray1(arr: number[]): number {
  let sum = 0;
  for (let i = 0; i < arr.length; i++) {
    sum += arr[i];
  }
  return sum;
}

function sumArray2(arr: number[]): number {
  return arr.reduce((sum, num) => sum + num, 0);
}
```

By identifying and refactoring these types of duplication, developers can improve code maintainability, reduce errors, and make the codebase more flexible for future changes[^1_1][^1_3].

## What about Temporal Duplication? And Duplication between Tests and Implementation

Kent Beck identifies several types of duplication that need refactoring, including temporal duplication and duplication between tests and implementation.

### Temporal Duplication

Temporal duplication refers to code that takes a long time to understand or execute, indicating a need for refactoring[^2_9]. Signs of temporal duplication include:

1. Code that takes more than a few seconds to comprehend
2. Methods or functions that are too long
3. Variables or methods with unclear purposes

Refactoring techniques for temporal duplication include:

- Renaming variables and methods for clarity
- Extracting methods to improve readability and reusability
- Applying the Compose Method refactoring for long methods

### Duplication Between Tests and Implementation

This type of duplication is a key focus in Test-Driven Development (TDD)[^2_1][^2_5]. It occurs when:

1. The test code closely mirrors the implementation code
2. There are hard-coded values in both test and production code

Addressing this duplication is crucial because:

- It indicates that the implementation might be incomplete or overly simplistic
- Removing it often leads to better design and more robust code

To eliminate duplication between tests and implementation:

1. Start with a simple, possibly hard-coded implementation to pass the initial test
2. Gradually replace constants with variables in the implementation
3. Refactor the code to remove duplication, making it more general and flexible

Kent Beck emphasizes that refactoring to remove duplication, especially between tests and implementation, is a fundamental part of the TDD cycle (Red/Green/Refactor)[^2_3][^2_5].

By addressing these types of duplication, developers can improve code clarity, maintainability, and design quality.

## What Does J. B. Rainsberger Say about Duplication

J. B. Rainsberger emphasizes the importance of removing duplication in code as a key aspect of refactoring and improving software design. He makes several significant points about duplication:

1. Mastery of removing duplication is crucial for object-oriented design. Rainsberger claims, "If you master removing duplication and fixing bad names, then I claim you master object-oriented design"[^3_5].
2. Duplication goes beyond just repeated lines of code. It includes duplicated logic, data, and even design decisions[^3_5].
3. Removing duplication can lead to better code organization and reveal underlying design principles. Rainsberger connects this to David Parnas' idea of hiding design decisions in modules[^3_5].
4. Rainsberger includes "minimizes duplication" as the second of his four "Elements of Simple Design"[^3_7].
5. He advocates for starting small when refactoring, often beginning with "tidyings" like improving variable names or removing unnecessary nesting, which can lead to identifying and removing more significant duplication[^3_1].
6. Rainsberger suggests that removing duplication can help in understanding the code better and may reveal new design possibilities[^3_1].

By focusing on removing duplication, Rainsberger argues that developers can improve code quality, maintainability, and overall design structure.

## What is David Parnas' Idea of Hiding Design Decisions in Modules

David Parnas introduced the concept of information hiding as a key principle in modular design. His idea of hiding design decisions in modules involves:

1. Identifying difficult design decisions or those likely to change in the future[^4_1][^4_3].
2. Designing each module to encapsulate and hide a specific design decision from other modules[^4_1][^4_3].
3. Creating abstract interfaces for modules that reveal only the necessary information while obscuring implementation details[^4_3].

This approach aims to achieve several goals:

1. Enable independent development of modules[^4_3].
2. Allow changes to one module without affecting others[^4_3].
3. Improve system comprehensibility by allowing developers to focus on one module at a time[^4_1].

Parnas argued against the common practice of decomposing systems based on flowcharts or processing steps. Instead, he proposed that modules should be designed around design decisions, not steps in processing[^4_5][^4_9].

The benefits of this approach include:

1. Improved flexibility and maintainability of the system[^4_9].
2. Reduced impact of changes, as design decisions are isolated within modules[^4_3].
3. Better organization of code and revelation of underlying design principles[^4_7].

Parnas' concept of information hiding has become a fundamental principle in software engineering and object-oriented design, influencing modern approaches to modular and maintainable software development[^4_4].
