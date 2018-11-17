const protobuf = require("protobufjs")
const fs = require('fs');

protobuf.load("../protobufs.proto", function(err, root) {
    if (err)
        throw err;

    // Obtain a message type
    var Config = root.lookupType("gaia.Config");

    binary = fs.readFileSync('out_python')

    console.log(binary)

    // Decode an Uint8Array (browser) or Buffer (node) to a message
    var message = Config.decode(binary);
    // ... do something with message

    console.log(message)
});