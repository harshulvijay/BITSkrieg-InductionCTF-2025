package ctf.induction.androidRev;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.nio.charset.StandardCharsets;


public class FlagActivity extends AppCompatActivity {
  public static byte[] hexToBytes(String hex) {
    if (hex == null || hex.length() % 2 != 0) {
      throw new IllegalArgumentException("Hex string must be non-null and have even length");
    }

    int len = hex.length();
    byte[] result = new byte[len / 2];

    for (int i = 0; i < len; i += 2) {
      int firstDigit = Character.digit(hex.charAt(i), 16);
      int secondDigit = Character.digit(hex.charAt(i + 1), 16);

      if (firstDigit == -1 || secondDigit == -1) {
        throw new IllegalArgumentException("Invalid hex character at position " + i);
      }

      result[i / 2] = (byte) ((firstDigit << 4) + secondDigit);
    }

    return result;
  }

  public static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
      sb.append(String.format("%02x", b));
    }
    return sb.toString();
  }

  /**
   * XORs two hex strings, repeating the shorter one until it matches the length of the longer.
   */
  public static String xorHexStrings(String hex1, String hex2) {
    byte[] bytes1 = hexToBytes(hex1);
    byte[] bytes2 = hexToBytes(hex2);

    // Decide max length
    int maxLen = Math.max(bytes1.length, bytes2.length);
    byte[] result = new byte[maxLen];

    for (int i = 0; i < maxLen; i++) {
      byte b1 = bytes1[i % bytes1.length]; // repeat if needed
      byte b2 = bytes2[i % bytes2.length]; // repeat if needed
      result[i] = (byte) (b1 ^ b2);
    }

    return bytesToHex(result);
  }

  /** Converts a hex string into a UTF-8 Java String */
  public static String hexToString(String hex) {
    byte[] bytes = hexToBytes(hex);
    return new String(bytes, StandardCharsets.UTF_8);
  }

  public void decryptFlag() {
    String encryptedFlag = getString(R.string.encrypted_flag_hex);
    String decryptedFlagHex = xorHexStrings(encryptedFlag,
      "73696d706c65786f72");
    String flag = hexToString(decryptedFlagHex);
  }

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    EdgeToEdge.enable(this);
    setContentView(R.layout.activity_flag);
    ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
      Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
      v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
      return insets;
    });
    decryptFlag();
  }
}