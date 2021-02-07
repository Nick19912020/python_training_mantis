import string
import random


def random_string(prefix, maxlen):
    symbol = string.ascii_letters
    return prefix + "".join([random.choice(symbol) for i in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    username = random_string("user_", 10)
    email = username + "@localhost"
    password = 'test'
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)