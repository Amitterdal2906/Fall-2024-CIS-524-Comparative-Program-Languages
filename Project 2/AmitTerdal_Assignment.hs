-- AmitTerdal_Assignment.hs
-- Haskell Programming Assignment Solutions

import Data.Char (toLower, isAlpha)

-- 1. Factorial function
-- This function calculates the factorial of a given integer n.
-- It handles edge cases like 0 (returns 1) and negative numbers (returns an error).

factorial :: Integer -> Integer
factorial n
    | n < 0     = error "Factorial not defined for negative numbers"
    | n == 0    = 1
    | otherwise = n * factorial (n - 1)

-- Test case for factorial function
-- factorial 5 should return 120
-- factorial 0 should return 1

-- 2. Prime check function
-- This function checks if a given positive integer is a prime number.

isPrime :: Integer -> Bool
isPrime n
    | n < 2     = False
    | otherwise = null [x | x <- [2 .. n-1], n `mod` x == 0]

-- Test case for isPrime function
-- isPrime 7 should return True
-- isPrime 4 should return False

-- 3. Fibonacci function
-- This function generates the nth Fibonacci number using recursion.
-- Edge cases: fibonacci 0 = 0 and fibonacci 1 = 1.

fibonacci :: Integer -> Integer
fibonacci n
    | n < 0     = error "Fibonacci not defined for negative numbers"
    | n == 0    = 0
    | n == 1    = 1
    | otherwise = fibonacci (n - 1) + fibonacci (n - 2)

-- Test case for fibonacci function
-- fibonacci 6 should return 8
-- fibonacci 0 should return 0

-- 4. Reverse list function
-- This function reverses a list (or string) using recursion.

reverseList :: [a] -> [a]
reverseList [] = []
reverseList (x:xs) = reverseList xs ++ [x]

-- Test case for reverseList function
-- reverseList [1, 2, 3] should return [3, 2, 1]
-- reverseList "hello" should return "olleh"

-- 5. Palindrome check function
-- This function checks if a given string is a palindrome, ignoring spaces and case sensitivity.

isPalindrome :: String -> Bool
isPalindrome str = cleaned == reverse cleaned
    where cleaned = map toLower (filter isAlpha str)

-- Test case for isPalindrome function
-- isPalindrome "A man a plan a canal Panama" should return True
-- isPalindrome "Hello" should return False


main :: IO ()
main = do
    putStrLn "-- 1. Factorial function"
    putStrLn "-- This function calculates the factorial of a given integer n (5)."
    putStrLn "-- It handles edge cases like 0 (returns 1) and negative numbers (returns an error).\n"
    print (factorial 5)
    putStrLn "\n"

    putStrLn "-- 2. Prime check function"
    putStrLn "-- This function checks if a given positive integer (7) is a prime number.\n"
    print (isPrime 7)
    putStrLn "\n"

    putStrLn "-- 3. Fibonacci function"
    putStrLn "-- This function generates the nth Fibonacci number using recursion."
    putStrLn "-- Edge cases: fibonacci 0 = 0 and fibonacci 1 = 1.\n"
    print (fibonacci 6)
    putStrLn "\n"

    putStrLn "-- 4. Reverse list function"
    putStrLn "-- This function reverses a list (or string) using recursion.\n"
    print (reverseList [1, 2, 3])
    putStrLn "\n"

    putStrLn "-- 5. Palindrome check function"
    putStrLn "-- This function checks if a given string is a palindrome, ignoring spaces and case sensitivity.\n"
    print (isPalindrome "A man a plan a canal Panama")
    putStrLn "\n"