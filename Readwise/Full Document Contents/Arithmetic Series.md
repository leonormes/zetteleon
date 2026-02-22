# Arithmetic Series

![rw-book-cover](https://media.geeksforgeeks.org/wp-content/cdn-uploads/gfg_200x200-min.png)

## Metadata
- Author: [[GeeksforGeeks]]
- Full Title: Arithmetic Series
- Category: #articles
- Summary: An arithmetic series is the sum of numbers in a sequence where each number increases by the same amount. The sum of the first n terms can be found using the formula Sn = n/2 [2a + (n−1)d]. Arithmetic series are used in savings, loan payments, inventory, depreciation, and algorithm analysis.
- URL: https://www.geeksforgeeks.org/arithmetic-series/

## Full Document
An ****arithmetic series**** is the sum of the terms of an ****arithmetic sequence****, where an arithmetic sequence is a sequence of numbers in which the difference between consecutive terms is constant.

Or we can say that an arithmetic progression can be defined as a sequence of numbers in which for every pair of consecutive terms, the second number is found by adding a constant number to the previous one.

Some examples includes:

* 2 + 4 + 6 + 8 + 10 + . . . + 2n
* 10 + 7 + 4 + 1−2−5 + . . . + (13 -3n)
* 1 + 4 + 7 + 10 + 13 + . . . + (3n − 2)

> ****Note:**** If a, a + d, a + 2d, a + 3d, . . . is arithmetic sequence then a + (a + d) + (a + 2d) + (a + 3d) + . . . is arithmetic series.
> 
> 

There are two major formulas related to the terms of Arithmetic Series:

* nth term, and
* Sum of first n Terms.

##### nth term of Arithmetic Series

The formula for nth term is,

> ****a********n**** ****= a + (n−1)d****
> 
> where,
> 
> * ****a**** is the first term
> * ****d**** is the common difference
> * ****n**** is the number of terms
> * ****a********n**** is the nth term
> 

#####  Sum of First n Terms

The sum of first “n” terms of the series can be easily found is we know the first term of the series and total terms. The formula for finding the sum of first "n" terms is:

****S********n**** ****= n/2 [2a + (n−1)d]****

where,

* ****a**** is the first term
* ****d**** is the common difference
* ****n**** is the number of terms.

> ****Note:**** The terms of an arithmetic sequence look like this: a, a + d, a + 2d, a + 3d, . . . , a + (n − 1)d
> 
> The sum of the first n terms of this sequence, Sn​, can be written as:
> 
> Sn = a + (a + d) + (a + 2d) + (a + 3d) + . . . +[a + (n − 1)d]
> 
> ⇒ Sn = [a+(n−1)d] + [a+(n−2)d] + . . . + a
> 
> Now, add these two expressions for Sn​ term by term:
> 
> 2Sn = (a+[a+(n−1)d]) + ((a+d)+[a+(n−2)d]) + . . . + ([a+(n−1)d]+a)
> 
> Each pair of terms in parentheses sums to the same value i.e., a+[a+(n−1)d] = 2a+(n−1)d
> 
> Thus, 2Sn = n ⋅ [2a + (n − 1)d]
> 
> ****S********n**** ****= (n/2) ⋅ [2a + (n − 1)d]****
> 
> 

##### Sigma Notation for Arithmetic Series

Using sigma notation, the sum of the first n terms of an arithmetic series can be expressed as:

S\_n = \sum\_{k=0}^{n-1} (a + kd)

Where,

* ∑ indicates that we are summing terms.
* k is the index of summation, starting from 0 and going up to n−1.
* a + kd is the general term of the arithmetic series, where k increments with each term.

****For Example: Σ********10********n=1**** ****(3n+7)**** 

Here the value of n starts with ‘1’ and ends at ’10’. When we start putting the value of n we get the arithmetic series just like below:

* 10 + 13 + 16 + 19 + . . . + 37

#### Recursive Formula

Recursive Formula gives to two information:

* First term of the sequence
* Pattern rule to find any term from the term that comes before it

Suppose, we have the series 3, 5, 7..... then here the first term of the series is a1 = 3 Now, from above the series we see that the formula for an Will be as below:

If a1 = 3 than an = a(n-1) + 2

Therefore, we have to add '2' to the previous term to get to next term of the series. Hence, finding the rest of the term below:

* a1 = 3
* a2 = a1+2 = 3 + 2 = 5
* a3 = a2 + 2 = 5 + 2 = 7
* a4 = a3 + 2 = 7 + 2 = 9
* a5 = a4 + 2 = 11... and so on.

#### Applications of Arithmetic Series

Arithmetic series have many practical applications across different fields, as they involve the sum of terms that increase or decrease by a constant amount. Here are some common applications:

* If someone saves or invests a fixed amount of money at regular intervals (e.g., monthly deposits), the total savings or investment over time can be calculated using an arithmetic series.
* Many loan repayments are based on regular, fixed payments, which can be represented by an arithmetic series to calculate the total amount paid over time.
* Businesses often replenish stock at a constant rate. Using an arithmetic series, they can calculate total inventory over time or assess total purchasing costs.
* In some cases, assets depreciate in value by a fixed amount every year, which is an arithmetic series. Summing the depreciation over several years helps businesses track the cumulative decrease in asset value.
* Many algorithms have steps that involve operations in an arithmetic sequence (e.g., searching or sorting algorithms). Analyzing the time complexity of such algorithms may require summing an arithmetic series.

****Related Articles****
