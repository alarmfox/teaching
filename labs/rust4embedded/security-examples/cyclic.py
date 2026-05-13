# To run this script install pwntools with pip install pwn
import pwn

# generate a sequence with 8-byte
seq = pwn.cyclic_gen(n=8)

# create a 1024 byte sequence long
input = seq.get(1024)
print(input)

# Retrieve the "buffer length", where the EIP registers points to
print(seq.find(b"aaaaaaek"))
