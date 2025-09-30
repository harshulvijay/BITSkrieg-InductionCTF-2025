**Writeup: PNG, who's there?**

**Challenge Overview:**
1) A binary file, Challenge.bin, contains concatenated PNG data.
2) It includes PNG file headers and IEND footers for 34 embedded PNGs.
3) Extracting each PNG yields 34 images, each displaying a single character.
4) Goal: Reconstruct the flag by ordering these characters correctly.


**Approach**:
1) Opening the file in hexedit or similar tools shows the following:

unsigned char ucDataBlock[37] = {

	// Offset 0x00000000 to 0x00000024

	0x57, 0x65, 0x6C, 0x63, 0x6F, 0x6D, 0x65, 0x20, 0x74, 0x6F, 0x20, 0x42,

	0x49, 0x54, 0x53, 0x6B, 0x72, 0x69, 0x65, 0x67, 0x0A, 0x89, 0x50, 0x4E,

	0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44,

	0x52

};

OR 

Welcome to BITSkrieg
PNG
*...more data...*
IEND
*...more PNG headers and endings*

2) From this, it is clear that there are multiple PNG files embedded into the binary file.

3) We need to extract all the files to get the flag.

4) You can do this manually by copying each PNG's bytes(Header: 89 50 4E 47 0D 0A 1A 0A, IEND: 49 45 4E 44 AE 42 60 82)

OR

4) You can write a python script to extract each PNG and push them into a folder using this script: 

```
import os

bin\_file = r"C\\input\_dir\\challenge.bin"
output\_dir = r"C\\output\_dir\\extracted\_images"

os.makedirs(output\_dir, exist\_ok=True)

with open(bin\_file, "rb") as f:

   data = f.read()

png\_header = b'\\x89PNG\\r\\n\\x1a\\n' # HEX: PNG

png\_footer = b'\\x49\\x45\\x4E\\x44\\xAE\\x42\\x60\\x82'  # HEX: IEND 

count = 0

i = 0
while True:
   start = data.find(png\_header, i)

   if start == -1:
       break

   end = data.find(png\_footer, start)

   if end == -1:
       break

   end += len(png\_footer)
   png\_data = data\[start:end]
   out\_path = os.path.join(output\_dir, f"extracted\_{count}.png")

   with open(out\_path, "wb") as out\_file:
       out\_file.write(png\_data)

   print(f"Extracted {out\_path}")

   count += 1
   i = end 

print(f"Done. Extracted {count} PNGs.")
```

5) The images are extracted into "extracted_images" directory

6) The letters inside the images correspond to the flag letters: InductionCTF{bin\_there\_hexed\_that}