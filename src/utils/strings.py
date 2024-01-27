import random
import string

def generate_random_string(length=21):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
