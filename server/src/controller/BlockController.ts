import { Body, Controller, Get, Param, Post } from 'routing-controllers';
import { Block } from '../entity/Block';
import { ControllerWithDB } from './ControllerWithDB';
import * as crypto from 'crypto';
import { Sign, Verify } from 'ed25519';

@Controller()
export class BlockController extends ControllerWithDB {

    /* API */
    @Get('/api/blocks')
    public async getAll() {
        return await this.db.blocks.find();
    }

    @Get('/api/blocks/:id')
    public async getOne(@Param('id') id: number) {
       return await this.db.blocks.findOne(id);
    }

    @Get('/api/blocks/new/:data')
    public async post(@Param('data') data: string) {

        const blocks = await this.db.blocks.find({ order: { id: 'DESC'} as any, take: 5});

        // find old block
        let oldBlock: Block;
        if (blocks.length > 0) {
            oldBlock = blocks[0];
        }

        const newBlock = this.db.blocks.create();

        // if genesis block, behave differently
        if (oldBlock === undefined) {
            newBlock.id = 0;
            newBlock.timestamp = new Date();
            newBlock.previousId = -1;
            newBlock.previousHash = '';
            newBlock.data = data.trim();
            newBlock.hash = newBlock.computeHash();
            console.log(newBlock);
        }

        /*
        try {
            const user = this.db.blocks.create();
            // user.unpackData(formData);
            const userInDB = await this.db.blocks.save(user);
            return userInDB;
        } catch (err) {
            console.log('We\'ve got a problem:', err);
        }
        */
    }
}
