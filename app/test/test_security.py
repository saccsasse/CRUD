from app.core.security import hash_password, verify_password

plain = "mypassword123"
hashed = hash_password(plain)
print("Hashed:", hashed)

assert verify_password(plain, hashed)  # should be True
assert not verify_password("wrongpass", hashed)  # should be False

print("Security functions work")