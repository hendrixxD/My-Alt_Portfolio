#!/usr/bin/env python3
"""
a main script to test Expense class
"""
import random
from faker import Faker
from expense import Expense

# Create a Faker instance
fake = Faker()

def generate_fake_expense():
    """
    Generate fake expense data using Faker.
    """
     # Generate a fake word for the title
    title = fake.word()
    # Generate a random amount between 10 and 1000
    amount = random.uniform(20000, 1000_000)
    
    return title, amount


if __name__=='__main__':
    # Generate 5 fake expenses for demonstration
    # for _ in range(3):
        #title, amount = generate_fake_expense()
        #exp = Expense(title=title, amount=f"{amount:.2f}")
        #print(exp.to_dict())
    

    #for title, amount in zip(title, amount):
    #    exp = Expense(title=title, amount=amount)
    #    
    #    print(exp.to_dict())
    
    exp = Expense(title="House Hold Items", amount=200_000.43)
    print(exp.to_dict())
    print()
    print()
    exp.update(title="Housing items")
    print(exp.to_dict())
    print()
    print()
    exp.update(amount=198_000.977)
    print(exp.to_dict())
    
