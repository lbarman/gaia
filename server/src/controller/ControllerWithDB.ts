import { getConnection, Repository } from 'typeorm';
import { Block } from '../entity/Block';

export interface IDatabase {
    blocks: Repository<Block>;
}

export class ControllerWithDB {

    public db: IDatabase;

    constructor() {
        const blockRepo: Repository<Block> = getConnection().getRepository(Block);

        this.db = {
            blocks: blockRepo
        };
    }
}
