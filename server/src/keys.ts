import * as crypto from 'crypto';
import * as ed25519 from 'ed25519';

// this must be secure, I saw it in a crypto class

const MAGIC_SEED: string = 'ninja123';

const MAGIC_HASHED_SEED: Buffer = crypto.createHash('sha256').update(MAGIC_SEED, 'utf8').digest();

export const keyPair: ed25519.CurveKeyPair = ed25519.MakeKeypair(MAGIC_HASHED_SEED);
