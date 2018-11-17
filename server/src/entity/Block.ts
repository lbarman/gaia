import * as crypto from 'crypto';
import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import * as ed25519 from 'ed25519';
import { keyPair } from '../keys';

@Entity()
export class Block {

    @PrimaryGeneratedColumn()
    public id: number;

    @Column({ nullable: false, default: '' })
    public timestamp: Date;

    @Column({ nullable: false, default: -1 })
    public data: string;

    @Column()
    public previousId: number;

    @Column({ nullable: false, default: '' })
    public previousHash: string;

    @Column({ nullable: false, default: '' })
    public hash: string;
    // btw, here the signature and the hash somehow play the same role, but I kept the "hash" as it is a core concept in the blockchain;
    // what we really have here is a permissioned blockchained without (real) proof-of-work, hence the hash is not strictly 
    // necessary to link blocks.

    // signature not included in hash
    @Column({ nullable: false, default: '' })
    public signature: string;

    public isProofOfWorkValid(): boolean {
        return false;
    }

    public toString(): string {
        const values: string[] = [];
        values.push(this.id.toString());
        values.push(this.timestamp.toString());
        values.push(this.data);
        values.push(this.hash);
        values.push(this.previousId.toString());
        values.push(this.previousHash);
        values.push(this.signature);

        return values.join('||');
    }

    public computeHash(): string {
        const values: string[] = [];
        values.push(this.id.toString());
        values.push(this.timestamp.toString());
        values.push(this.data);
        values.push(this.previousId.toString());
        values.push(this.previousHash);

        const str = values.join('||');
        const hash = crypto.createHash('sha256').update(str, 'utf8').digest();
        return hash.toString('hex');
    }

    public sign(key: ed25519.CurveKeyPair) {
        const str = this.signingData();
        const sig = ed25519.Sign(new Buffer(str, 'utf-8'), key);
        return sig.toString('hex');
    }

    public verify(key: ed25519.CurveKeyPair) {
        const str = this.signingData();
        const sig = ed25519.Verify(new Buffer(str, 'utf-8'), key);
        return sig.toString('hex');
    }

    private signingData(): string {
        const values: string[] = [];
        values.push(this.id.toString());
        values.push(this.timestamp.toString());
        values.push(this.data);
        values.push(this.previousId.toString());
        values.push(this.previousHash);
        values.push(this.hash);

        const str = values.join('||');
        return str;
    }
}
