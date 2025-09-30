**Challenge: Beeps per minute**

**Overview**
We’re given a .wav file as the challenge artifact. On listening, it’s not a normal song. Instead, it plays short segments of the “wiggly wobbly woo” meme song, but the segments sound chopped and placed in a specific repeating order.

Each distinct sound from the song corresponds to a symbol in Morse code:
Wiggly → . (dot)
Wobbly → - (dash)
Woo → ' ' (space / separator)

So the audio isn’t random: it’s Morse encoded with meme segments.

**Process**
Listen through the audio and identify where each piece (“wiggly”, “wobbly”, “woo”) occurs.
Translate these into Morse symbols:
Mark “wiggly” as a dot (.).
Mark “wobbly” as a dash (-).
Use “woo” to split letters or words.
Collect the full sequence of dots, dashes, and spaces.
Feed the sequence into a Morse code translator tool (e.g., MorseCode.World or manual decoding).

The Morse sequence spells out:
m0rs3_r0t

Thus, the flag is:
InductionCTF{m0rs3_r0t}