import * as bodyParser from 'body-parser';
import * as express from 'express';
import 'reflect-metadata';
import { useExpressServer } from 'routing-controllers';
import { Connection, createConnection } from 'typeorm';
import { SERVER_PORT } from './constants';
import { BlockController } from './controller/BlockController';
import indexTpl from './view/index.top';
import { Block } from './entity/Block';
import { keyPair } from './keys';
import * as ed25519 from 'ed25519';


createConnection().then(async (connection: Connection) => {

    const app = express();

    /*
    app.disable('x-powered-by');
    app.use((_, res, next) => {
        res.setHeader('Content-Security-Policy', 'default-src \'self\' \'unsafe-inline\'; script-src \'self\' \'unsafe-inline\' cdnjs.cloudflare.com code.jquery.com cloud.tinymce.com cdn.plot.ly; style-src \'self\' \'unsafe-inline\' cdnjs.cloudflare.com');
        return next();
    });
    */

    const db = connection.getRepository(Block);
    const b = db.create();
    b.id = 1;
    b.data = '10.1|12.2';
    b.timestamp = new Date();
    b.previousId = -1;
    b.previousHash = '';
    b.hash = b.computeHash();
    b.signWithKey(keyPair);

    b.
    await db.save(b);

    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));

    // import our controllers
    useExpressServer(app, {
        controllers: [BlockController]
    });

    // set the Assets routes
    app.use('/public', express.static('./src/public/'));
    app.use('/css', express.static('./src/public/css'));
    app.use('/img', express.static('./src/public/img'));
    app.use('/js', express.static('./src/public/js'));

    // set the default route
    app.get('/', (req: express.Request, res: express.Response) => {
        res.send(indexTpl());
    });

    // start express server
    app.listen(SERVER_PORT);
    console.log(`Server listening on port ${SERVER_PORT}`);
});
