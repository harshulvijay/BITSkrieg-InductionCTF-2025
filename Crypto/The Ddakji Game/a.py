from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
ascii_string = "y0u_h4ve_b33n_chos3n_by_the_m4sked_gu4rds_survival_is_3ss3n7i4l_4wait_47_InductionCTF{r4v3nhill_gr0unds_a7_midnigh7}_f0r_the_squid_g4me"
bytes_object = ascii_string.encode('ascii')
a = bytes_to_long(bytes_object)
print(f"Original string: {ascii_string}")
print(f"Converted bytes: {bytes_object}")
print(f"Type of converted object: {type(bytes_object)}")
print(bytes_to_long(bytes_object))
print(a.bit_length)
print(long_to_bytes(a))
