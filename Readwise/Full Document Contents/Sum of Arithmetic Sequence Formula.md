# Sum of Arithmetic Sequence Formula

![rw-book-cover](https://media.geeksforgeeks.org/wp-content/cdn-uploads/gfg_200x200-min.png)

## Metadata
- Author: [[GeeksforGeeks]]
- Full Title: Sum of Arithmetic Sequence Formula
- Category: #articles
- Summary: An arithmetic sequence is a list of numbers with a constant difference between terms. The sum of the first n terms can be found using the formula Sn = n/2 × (2a + (n − 1)d) or Sn = n/2 × (a + an). This formula helps calculate sums, first terms, common differences, and number of terms in such sequences.
- URL: https://www.geeksforgeeks.org/maths/sum-of-arithmetic-sequence-formula/

## Full Document
An ****arithmetic sequence**** is a number series in which each subsequent term is the sum of its preceding term and a constant integer.   

This constant number is referred to as the ****common difference****. As a result, the differences between every two successive terms in an arithmetic series are the same.

> If the first term of an arithmetic sequence is a and the common difference is d, then the terms of the arithmetic sequence are of the form:
> 
>  ****a, a + d, a + 2d, a + 3d, a + 4d, ....****
> 
> 

##### ****Sum of the Arithmetic Sequence****

We can calculate the sum of all terms in an arithmetic sequence using the sum of the arithmetic sequence formula.  

When an arithmetic sequence is expressed as the sum of its terms, such as a + (a + d) + (a + 2d) + (a + 3d) +…, it is referred to as an [arithmetic series](https://www.geeksforgeeks.org/arithmetic-series/).  

The ****formula for the sum of the n terms**** of an arithmetic series when the last term is not given is:

![2-min-1](https://media.geeksforgeeks.org/wp-content/uploads/20240723172025/2-min-1.png)
##### The formula for Sum When Last Term is Given:

The formula for the sum of the first n terms of an arithmetic sequence is:

****S********n**** ****= n/2 ⋅ (2a + (n − 1)d)****

If we write 2a as a + a, the formula becomes:

****S********n**** ****= n/2 ⋅ (a + a + (n − 1) d)****

Recognizing that ****a + (n − 1)d = a********n****, we get:

> ****S********n**** ****= n/2 ⋅ (a + a********n********)****
> 
> 

Where:

* Sn​ is the sum of the first n terms.
* a is the first term.
* an is the last term.
* n is the number of terms.

****This formula is useful when the last term (a********n********) is given.****

##### ****Derivation****

> Suppose the first term of a sequence is a, common difference is d and the number of terms are n.
> 
> We know the nth term of the sequence is given by, 
> 
> an = a + (n - 1)d ...... (1)
> 
> Also the sum of the arithmetic sequence is,  
> Sn = a + (a + d) + (a + 2d) + (a + 3d) + ...... + a + (n - 1)d ...... (2)
> 
> From (1), the equation (2) can also be expressed as,  
> Sn = an + an - d + an - 2d + an - 3d + ...... + an - (n - 1)d ...... (3)
> 
> Adding (2) and (3) we get,  
> 2 Sn = [a + (a + d) + (a + 2d) + (a + 3d) + ...... + a + (n - 1)d] + [an + an - d + an - 2d + an - 3d + ...... + an - (n - 1)d]  
> 2 Sn = (a + a + a + ..... n times) + (an + an + an + ..... n times)  
> 2 Sn = n (a + an)
> 
> ****S********n**** ****= n/2 [a + a********n********]****
> 
> This derives the formula for sum of an arithmetic sequence.
> 
> 

##### ****Sample Questions****

****Question 1. Find the sum of the arithmetic sequence: 4, 10, 16, 22, ...... up to 10 terms.****

****Solution:****

> We have, a = 4, d = 10 - 4 = 6 and n = 10.
> 
> Use the formula Sn = n/2 [2a + (n - 1)d] to find the required sum.
> 
> S10 = 10/2 [2(4) + (10 - 1)6]  
> = 5 (8 + 54)  
> = 5 (62)  
> = 310
> 
> 

****Question 2. Find the sum of the arithmetic sequence: 7, 9, 11, 13, ...... up to 15 terms.****

****Solution:****

> We have, a = 7, d = 9 - 7 = 2 and n = 15.
> 
> Use the formula Sn = n/2 [2a + (n - 1)d] to find the required sum.  
> S15 = 15/2 [2(7) + (15 - 1)2]  
> = 15/2 (14 + 28)  
> = 15/2 (42)  
> = 315
> 
> 

****Question 3. Find the first term of an arithmetic sequence if it has a sum of 240 for a common difference of 2 between 12 terms.****

****Solution:****

> We have, Sn = 240, d = 2 and n = 12.
> 
> Use the formula Sn = n/2 [2a + (n - 1)d] to find the required value.  
> => 240 = 12/2 [2a + (12 - 1)2]  
> => 240 = 6 (2a + 22)  
> => 40 = 2a + 22  
> => 2a = 18  
> => a = 9 
> 
> 

****Question 4. Find the common difference of an arithmetic sequence of 8 terms having a sum of 116 and the first term as 4.****

****Solution:****

> We have, S = 116, a = 4, n = 8.
> 
> Use the formula Sn = n/2 [2a + (n - 1)d] to find the required value.  
> => 116 = 8/2 [2(4) + (8 - 1)d]  
> => 116 = 4 (8 + 7d)  
> => 29 = 8 + 7d  
> => 7d = 21  
> => d = 3
> 
> 

****Question 5. Find the sum of an arithmetic sequence of 8 terms with the********first and last terms as 4 and 10 respectively.****

****Solution:****

> We have, a = 4, n = 8 and an = 10.
> 
> Use the formula Sn = n/2 [a + an] to find the required sum.  
> S8 = 8/2 [4 + 10]  
> = 4 (14)  
> = 56
> 
> 

****Question 6. Find the number of terms of an arithmetic sequence with the first term, last term****, ****and sum as 16, 12, and 140 respectively.****

****Solution:****

> We have, S = 140, a = 16 and an = 12.
> 
> Use the formula Sn = n/2 [a + an] to find the required value.  
> => 140 = n/2 [16 + 12]  
> => 140 = n/2 (28)  
> => 14n = 140  
> => n = 10
> 
> 

****Question 7. Find the sum of an arithmetic sequence with the first term, common difference****, ****and last term as 8,**** ****7, and 50 respectively.****

****Solution:****

> We have, a = 8, d = 7 and an = 50.
> 
> Use the formula an = a + (n - 1)d to find n.  
> => 50 = 8 + (n - 1)7  
> => 42 = 7 (n - 1)  
> => n - 1 = 6  
> => n = 7
> 
> Use the formula Sn = n/2 [a + an] to find the sum of sequence.
> 
> S7 = 7/2 (8 + 50)  
> = 7/2 (58)  
> = 203
> 
>
