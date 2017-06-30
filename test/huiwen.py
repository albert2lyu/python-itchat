import re

def reverse(text):
    return text[::-1]


def is_palindrome(text):
    text = text.lower()
    text = re.sub(r'\s|,','',text)
    print(text)
    return text == reverse(text)


something = input("Enter text: ")
if is_palindrome(something):
    print("Yes, it is a palindrome")
else:
    print("No, it is not a palindrome")