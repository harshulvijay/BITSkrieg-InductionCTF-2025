# [rev] strings are cool &mdash; Write Up

## Decompiling the app

Use [jadx](https://github.com/skylot/jadx) to decompile the app.

## Making sense of the source

In `sources/ctf/induction/androidRev/FlagActivity.java`, we can see a function called `decryptFlag()`. It gets the encrypted flag using `R.string`, and then XORs it with another hard coded value ("73696d706c65786f72"). Then it converts the resultant hex value to string.

## Finding the encrypted flag

The encrypted flag is stored at `R.string.encrypted_flag`. These values are stored at `resources/res/values/strings.xml`.

## Getting the flag

XOR `encrypted_flag` (found in `resources/res/values/strings.xml`) with "73696d706c65786f72" (found in the source) to get the flag `InductionCTF{h3x_m4sk_r3v34ls_th3_truth}`
