// crypto.js
import forge from "node-forge";

// Decrypt PEM private key using password
export const rsaDecrypt = {
  decryptPrivateKey: async (pemText, password) => {
    try {
      
      const privateKey = forge.pki.decryptRsaPrivateKey(pemText, password);
      if (!privateKey) throw new Error("Invalid password or key");
      return privateKey;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
};

// AES-GCM decryption
export async function aesGcmDecrypt(nonceB64, ciphertextBytes, privateKey, encAesKeyB64) {
  try {
    // Decode AES key (wrapped with RSA)
    const encAesKeyBytes = forge.util.decode64(encAesKeyB64);
    const aesKeyBytes = privateKey.decrypt(encAesKeyBytes, "RSA-OAEP");

    const keyBuffer = new Uint8Array(aesKeyBytes.split("").map(c => c.charCodeAt(0)));

    const iv = Uint8Array.from(atob(nonceB64), c => c.charCodeAt(0));

    const cryptoKey = await crypto.subtle.importKey(
      "raw",
      keyBuffer,
      { name: "AES-GCM" },
      false,
      ["decrypt"]
    );

    const decrypted = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv },
      cryptoKey,
      ciphertextBytes
    );

    return new Uint8Array(decrypted);
  } catch (err) {
    console.error(err);
    throw err;
  }
}
