/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
"use strict";

var $protobuf = require("protobufjs/minimal");

// Common aliases
var $Reader = $protobuf.Reader, $Writer = $protobuf.Writer, $util = $protobuf.util;

// Exported root namespace
var $root = $protobuf.roots["default"] || ($protobuf.roots["default"] = {});

$root.gaia = (function() {

    /**
     * Namespace gaia.
     * @exports gaia
     * @namespace
     */
    var gaia = {};

    gaia.Config = (function() {

        /**
         * Properties of a Config.
         * @memberof gaia
         * @interface IConfig
         * @property {boolean|null} [feedingModuleActivated] Config feedingModuleActivated
         * @property {boolean|null} [wateringModuleActivated] Config wateringModuleActivated
         * @property {string|null} [feedingModuleCronstring] Config feedingModuleCronstring
         * @property {string|null} [wateringModuleCronstring] Config wateringModuleCronstring
         * @property {number|null} [wateringPump_1Duration] Config wateringPump_1Duration
         * @property {number|null} [wateringPump_2Duration] Config wateringPump_2Duration
         * @property {number|null} [wateringPump_3Duration] Config wateringPump_3Duration
         * @property {number|null} [wateringPump_4Duration] Config wateringPump_4Duration
         */

        /**
         * Constructs a new Config.
         * @memberof gaia
         * @classdesc Represents a Config.
         * @implements IConfig
         * @constructor
         * @param {gaia.IConfig=} [properties] Properties to set
         */
        function Config(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Config feedingModuleActivated.
         * @member {boolean} feedingModuleActivated
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.feedingModuleActivated = false;

        /**
         * Config wateringModuleActivated.
         * @member {boolean} wateringModuleActivated
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringModuleActivated = false;

        /**
         * Config feedingModuleCronstring.
         * @member {string} feedingModuleCronstring
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.feedingModuleCronstring = "";

        /**
         * Config wateringModuleCronstring.
         * @member {string} wateringModuleCronstring
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringModuleCronstring = "";

        /**
         * Config wateringPump_1Duration.
         * @member {number} wateringPump_1Duration
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringPump_1Duration = 0;

        /**
         * Config wateringPump_2Duration.
         * @member {number} wateringPump_2Duration
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringPump_2Duration = 0;

        /**
         * Config wateringPump_3Duration.
         * @member {number} wateringPump_3Duration
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringPump_3Duration = 0;

        /**
         * Config wateringPump_4Duration.
         * @member {number} wateringPump_4Duration
         * @memberof gaia.Config
         * @instance
         */
        Config.prototype.wateringPump_4Duration = 0;

        /**
         * Creates a new Config instance using the specified properties.
         * @function create
         * @memberof gaia.Config
         * @static
         * @param {gaia.IConfig=} [properties] Properties to set
         * @returns {gaia.Config} Config instance
         */
        Config.create = function create(properties) {
            return new Config(properties);
        };

        /**
         * Encodes the specified Config message. Does not implicitly {@link gaia.Config.verify|verify} messages.
         * @function encode
         * @memberof gaia.Config
         * @static
         * @param {gaia.IConfig} message Config message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Config.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.feedingModuleActivated != null && message.hasOwnProperty("feedingModuleActivated"))
                writer.uint32(/* id 1, wireType 0 =*/8).bool(message.feedingModuleActivated);
            if (message.wateringModuleActivated != null && message.hasOwnProperty("wateringModuleActivated"))
                writer.uint32(/* id 2, wireType 0 =*/16).bool(message.wateringModuleActivated);
            if (message.feedingModuleCronstring != null && message.hasOwnProperty("feedingModuleCronstring"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.feedingModuleCronstring);
            if (message.wateringModuleCronstring != null && message.hasOwnProperty("wateringModuleCronstring"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.wateringModuleCronstring);
            if (message.wateringPump_1Duration != null && message.hasOwnProperty("wateringPump_1Duration"))
                writer.uint32(/* id 5, wireType 0 =*/40).int32(message.wateringPump_1Duration);
            if (message.wateringPump_2Duration != null && message.hasOwnProperty("wateringPump_2Duration"))
                writer.uint32(/* id 6, wireType 0 =*/48).int32(message.wateringPump_2Duration);
            if (message.wateringPump_3Duration != null && message.hasOwnProperty("wateringPump_3Duration"))
                writer.uint32(/* id 7, wireType 0 =*/56).int32(message.wateringPump_3Duration);
            if (message.wateringPump_4Duration != null && message.hasOwnProperty("wateringPump_4Duration"))
                writer.uint32(/* id 8, wireType 0 =*/64).int32(message.wateringPump_4Duration);
            return writer;
        };

        /**
         * Encodes the specified Config message, length delimited. Does not implicitly {@link gaia.Config.verify|verify} messages.
         * @function encodeDelimited
         * @memberof gaia.Config
         * @static
         * @param {gaia.IConfig} message Config message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Config.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Config message from the specified reader or buffer.
         * @function decode
         * @memberof gaia.Config
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {gaia.Config} Config
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Config.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.gaia.Config();
            while (reader.pos < end) {
                var tag = reader.uint32();
                switch (tag >>> 3) {
                case 1:
                    message.feedingModuleActivated = reader.bool();
                    break;
                case 2:
                    message.wateringModuleActivated = reader.bool();
                    break;
                case 3:
                    message.feedingModuleCronstring = reader.string();
                    break;
                case 4:
                    message.wateringModuleCronstring = reader.string();
                    break;
                case 5:
                    message.wateringPump_1Duration = reader.int32();
                    break;
                case 6:
                    message.wateringPump_2Duration = reader.int32();
                    break;
                case 7:
                    message.wateringPump_3Duration = reader.int32();
                    break;
                case 8:
                    message.wateringPump_4Duration = reader.int32();
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Config message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof gaia.Config
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {gaia.Config} Config
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Config.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Config message.
         * @function verify
         * @memberof gaia.Config
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Config.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.feedingModuleActivated != null && message.hasOwnProperty("feedingModuleActivated"))
                if (typeof message.feedingModuleActivated !== "boolean")
                    return "feedingModuleActivated: boolean expected";
            if (message.wateringModuleActivated != null && message.hasOwnProperty("wateringModuleActivated"))
                if (typeof message.wateringModuleActivated !== "boolean")
                    return "wateringModuleActivated: boolean expected";
            if (message.feedingModuleCronstring != null && message.hasOwnProperty("feedingModuleCronstring"))
                if (!$util.isString(message.feedingModuleCronstring))
                    return "feedingModuleCronstring: string expected";
            if (message.wateringModuleCronstring != null && message.hasOwnProperty("wateringModuleCronstring"))
                if (!$util.isString(message.wateringModuleCronstring))
                    return "wateringModuleCronstring: string expected";
            if (message.wateringPump_1Duration != null && message.hasOwnProperty("wateringPump_1Duration"))
                if (!$util.isInteger(message.wateringPump_1Duration))
                    return "wateringPump_1Duration: integer expected";
            if (message.wateringPump_2Duration != null && message.hasOwnProperty("wateringPump_2Duration"))
                if (!$util.isInteger(message.wateringPump_2Duration))
                    return "wateringPump_2Duration: integer expected";
            if (message.wateringPump_3Duration != null && message.hasOwnProperty("wateringPump_3Duration"))
                if (!$util.isInteger(message.wateringPump_3Duration))
                    return "wateringPump_3Duration: integer expected";
            if (message.wateringPump_4Duration != null && message.hasOwnProperty("wateringPump_4Duration"))
                if (!$util.isInteger(message.wateringPump_4Duration))
                    return "wateringPump_4Duration: integer expected";
            return null;
        };

        /**
         * Creates a Config message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof gaia.Config
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {gaia.Config} Config
         */
        Config.fromObject = function fromObject(object) {
            if (object instanceof $root.gaia.Config)
                return object;
            var message = new $root.gaia.Config();
            if (object.feedingModuleActivated != null)
                message.feedingModuleActivated = Boolean(object.feedingModuleActivated);
            if (object.wateringModuleActivated != null)
                message.wateringModuleActivated = Boolean(object.wateringModuleActivated);
            if (object.feedingModuleCronstring != null)
                message.feedingModuleCronstring = String(object.feedingModuleCronstring);
            if (object.wateringModuleCronstring != null)
                message.wateringModuleCronstring = String(object.wateringModuleCronstring);
            if (object.wateringPump_1Duration != null)
                message.wateringPump_1Duration = object.wateringPump_1Duration | 0;
            if (object.wateringPump_2Duration != null)
                message.wateringPump_2Duration = object.wateringPump_2Duration | 0;
            if (object.wateringPump_3Duration != null)
                message.wateringPump_3Duration = object.wateringPump_3Duration | 0;
            if (object.wateringPump_4Duration != null)
                message.wateringPump_4Duration = object.wateringPump_4Duration | 0;
            return message;
        };

        /**
         * Creates a plain object from a Config message. Also converts values to other types if specified.
         * @function toObject
         * @memberof gaia.Config
         * @static
         * @param {gaia.Config} message Config
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Config.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.feedingModuleActivated = false;
                object.wateringModuleActivated = false;
                object.feedingModuleCronstring = "";
                object.wateringModuleCronstring = "";
                object.wateringPump_1Duration = 0;
                object.wateringPump_2Duration = 0;
                object.wateringPump_3Duration = 0;
                object.wateringPump_4Duration = 0;
            }
            if (message.feedingModuleActivated != null && message.hasOwnProperty("feedingModuleActivated"))
                object.feedingModuleActivated = message.feedingModuleActivated;
            if (message.wateringModuleActivated != null && message.hasOwnProperty("wateringModuleActivated"))
                object.wateringModuleActivated = message.wateringModuleActivated;
            if (message.feedingModuleCronstring != null && message.hasOwnProperty("feedingModuleCronstring"))
                object.feedingModuleCronstring = message.feedingModuleCronstring;
            if (message.wateringModuleCronstring != null && message.hasOwnProperty("wateringModuleCronstring"))
                object.wateringModuleCronstring = message.wateringModuleCronstring;
            if (message.wateringPump_1Duration != null && message.hasOwnProperty("wateringPump_1Duration"))
                object.wateringPump_1Duration = message.wateringPump_1Duration;
            if (message.wateringPump_2Duration != null && message.hasOwnProperty("wateringPump_2Duration"))
                object.wateringPump_2Duration = message.wateringPump_2Duration;
            if (message.wateringPump_3Duration != null && message.hasOwnProperty("wateringPump_3Duration"))
                object.wateringPump_3Duration = message.wateringPump_3Duration;
            if (message.wateringPump_4Duration != null && message.hasOwnProperty("wateringPump_4Duration"))
                object.wateringPump_4Duration = message.wateringPump_4Duration;
            return object;
        };

        /**
         * Converts this Config to JSON.
         * @function toJSON
         * @memberof gaia.Config
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Config.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        return Config;
    })();

    gaia.SystemStatus = (function() {

        /**
         * Properties of a SystemStatus.
         * @memberof gaia
         * @interface ISystemStatus
         * @property {string|null} [uptime] SystemStatus uptime
         * @property {string|null} [memory] SystemStatus memory
         * @property {string|null} [diskUsage] SystemStatus diskUsage
         * @property {string|null} [processes] SystemStatus processes
         */

        /**
         * Constructs a new SystemStatus.
         * @memberof gaia
         * @classdesc Represents a SystemStatus.
         * @implements ISystemStatus
         * @constructor
         * @param {gaia.ISystemStatus=} [properties] Properties to set
         */
        function SystemStatus(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * SystemStatus uptime.
         * @member {string} uptime
         * @memberof gaia.SystemStatus
         * @instance
         */
        SystemStatus.prototype.uptime = "";

        /**
         * SystemStatus memory.
         * @member {string} memory
         * @memberof gaia.SystemStatus
         * @instance
         */
        SystemStatus.prototype.memory = "";

        /**
         * SystemStatus diskUsage.
         * @member {string} diskUsage
         * @memberof gaia.SystemStatus
         * @instance
         */
        SystemStatus.prototype.diskUsage = "";

        /**
         * SystemStatus processes.
         * @member {string} processes
         * @memberof gaia.SystemStatus
         * @instance
         */
        SystemStatus.prototype.processes = "";

        /**
         * Creates a new SystemStatus instance using the specified properties.
         * @function create
         * @memberof gaia.SystemStatus
         * @static
         * @param {gaia.ISystemStatus=} [properties] Properties to set
         * @returns {gaia.SystemStatus} SystemStatus instance
         */
        SystemStatus.create = function create(properties) {
            return new SystemStatus(properties);
        };

        /**
         * Encodes the specified SystemStatus message. Does not implicitly {@link gaia.SystemStatus.verify|verify} messages.
         * @function encode
         * @memberof gaia.SystemStatus
         * @static
         * @param {gaia.ISystemStatus} message SystemStatus message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SystemStatus.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.uptime != null && message.hasOwnProperty("uptime"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.uptime);
            if (message.memory != null && message.hasOwnProperty("memory"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.memory);
            if (message.diskUsage != null && message.hasOwnProperty("diskUsage"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.diskUsage);
            if (message.processes != null && message.hasOwnProperty("processes"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.processes);
            return writer;
        };

        /**
         * Encodes the specified SystemStatus message, length delimited. Does not implicitly {@link gaia.SystemStatus.verify|verify} messages.
         * @function encodeDelimited
         * @memberof gaia.SystemStatus
         * @static
         * @param {gaia.ISystemStatus} message SystemStatus message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SystemStatus.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a SystemStatus message from the specified reader or buffer.
         * @function decode
         * @memberof gaia.SystemStatus
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {gaia.SystemStatus} SystemStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SystemStatus.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.gaia.SystemStatus();
            while (reader.pos < end) {
                var tag = reader.uint32();
                switch (tag >>> 3) {
                case 1:
                    message.uptime = reader.string();
                    break;
                case 2:
                    message.memory = reader.string();
                    break;
                case 3:
                    message.diskUsage = reader.string();
                    break;
                case 4:
                    message.processes = reader.string();
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a SystemStatus message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof gaia.SystemStatus
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {gaia.SystemStatus} SystemStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SystemStatus.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a SystemStatus message.
         * @function verify
         * @memberof gaia.SystemStatus
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        SystemStatus.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.uptime != null && message.hasOwnProperty("uptime"))
                if (!$util.isString(message.uptime))
                    return "uptime: string expected";
            if (message.memory != null && message.hasOwnProperty("memory"))
                if (!$util.isString(message.memory))
                    return "memory: string expected";
            if (message.diskUsage != null && message.hasOwnProperty("diskUsage"))
                if (!$util.isString(message.diskUsage))
                    return "diskUsage: string expected";
            if (message.processes != null && message.hasOwnProperty("processes"))
                if (!$util.isString(message.processes))
                    return "processes: string expected";
            return null;
        };

        /**
         * Creates a SystemStatus message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof gaia.SystemStatus
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {gaia.SystemStatus} SystemStatus
         */
        SystemStatus.fromObject = function fromObject(object) {
            if (object instanceof $root.gaia.SystemStatus)
                return object;
            var message = new $root.gaia.SystemStatus();
            if (object.uptime != null)
                message.uptime = String(object.uptime);
            if (object.memory != null)
                message.memory = String(object.memory);
            if (object.diskUsage != null)
                message.diskUsage = String(object.diskUsage);
            if (object.processes != null)
                message.processes = String(object.processes);
            return message;
        };

        /**
         * Creates a plain object from a SystemStatus message. Also converts values to other types if specified.
         * @function toObject
         * @memberof gaia.SystemStatus
         * @static
         * @param {gaia.SystemStatus} message SystemStatus
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        SystemStatus.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.uptime = "";
                object.memory = "";
                object.diskUsage = "";
                object.processes = "";
            }
            if (message.uptime != null && message.hasOwnProperty("uptime"))
                object.uptime = message.uptime;
            if (message.memory != null && message.hasOwnProperty("memory"))
                object.memory = message.memory;
            if (message.diskUsage != null && message.hasOwnProperty("diskUsage"))
                object.diskUsage = message.diskUsage;
            if (message.processes != null && message.hasOwnProperty("processes"))
                object.processes = message.processes;
            return object;
        };

        /**
         * Converts this SystemStatus to JSON.
         * @function toJSON
         * @memberof gaia.SystemStatus
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        SystemStatus.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        return SystemStatus;
    })();

    gaia.Status = (function() {

        /**
         * Properties of a Status.
         * @memberof gaia
         * @interface IStatus
         * @property {string|null} [authenticationToken] Status authenticationToken
         * @property {string|null} [localTimestamp] Status localTimestamp
         * @property {gaia.IConfig|null} [currentConfig] Status currentConfig
         * @property {gaia.ISystemStatus|null} [systemStatus] Status systemStatus
         */

        /**
         * Constructs a new Status.
         * @memberof gaia
         * @classdesc Represents a Status.
         * @implements IStatus
         * @constructor
         * @param {gaia.IStatus=} [properties] Properties to set
         */
        function Status(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Status authenticationToken.
         * @member {string} authenticationToken
         * @memberof gaia.Status
         * @instance
         */
        Status.prototype.authenticationToken = "";

        /**
         * Status localTimestamp.
         * @member {string} localTimestamp
         * @memberof gaia.Status
         * @instance
         */
        Status.prototype.localTimestamp = "";

        /**
         * Status currentConfig.
         * @member {gaia.IConfig|null|undefined} currentConfig
         * @memberof gaia.Status
         * @instance
         */
        Status.prototype.currentConfig = null;

        /**
         * Status systemStatus.
         * @member {gaia.ISystemStatus|null|undefined} systemStatus
         * @memberof gaia.Status
         * @instance
         */
        Status.prototype.systemStatus = null;

        /**
         * Creates a new Status instance using the specified properties.
         * @function create
         * @memberof gaia.Status
         * @static
         * @param {gaia.IStatus=} [properties] Properties to set
         * @returns {gaia.Status} Status instance
         */
        Status.create = function create(properties) {
            return new Status(properties);
        };

        /**
         * Encodes the specified Status message. Does not implicitly {@link gaia.Status.verify|verify} messages.
         * @function encode
         * @memberof gaia.Status
         * @static
         * @param {gaia.IStatus} message Status message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Status.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.authenticationToken != null && message.hasOwnProperty("authenticationToken"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.authenticationToken);
            if (message.localTimestamp != null && message.hasOwnProperty("localTimestamp"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.localTimestamp);
            if (message.currentConfig != null && message.hasOwnProperty("currentConfig"))
                $root.gaia.Config.encode(message.currentConfig, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.systemStatus != null && message.hasOwnProperty("systemStatus"))
                $root.gaia.SystemStatus.encode(message.systemStatus, writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified Status message, length delimited. Does not implicitly {@link gaia.Status.verify|verify} messages.
         * @function encodeDelimited
         * @memberof gaia.Status
         * @static
         * @param {gaia.IStatus} message Status message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Status.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Status message from the specified reader or buffer.
         * @function decode
         * @memberof gaia.Status
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {gaia.Status} Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Status.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.gaia.Status();
            while (reader.pos < end) {
                var tag = reader.uint32();
                switch (tag >>> 3) {
                case 1:
                    message.authenticationToken = reader.string();
                    break;
                case 2:
                    message.localTimestamp = reader.string();
                    break;
                case 3:
                    message.currentConfig = $root.gaia.Config.decode(reader, reader.uint32());
                    break;
                case 4:
                    message.systemStatus = $root.gaia.SystemStatus.decode(reader, reader.uint32());
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Status message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof gaia.Status
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {gaia.Status} Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Status.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Status message.
         * @function verify
         * @memberof gaia.Status
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Status.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.authenticationToken != null && message.hasOwnProperty("authenticationToken"))
                if (!$util.isString(message.authenticationToken))
                    return "authenticationToken: string expected";
            if (message.localTimestamp != null && message.hasOwnProperty("localTimestamp"))
                if (!$util.isString(message.localTimestamp))
                    return "localTimestamp: string expected";
            if (message.currentConfig != null && message.hasOwnProperty("currentConfig")) {
                var error = $root.gaia.Config.verify(message.currentConfig);
                if (error)
                    return "currentConfig." + error;
            }
            if (message.systemStatus != null && message.hasOwnProperty("systemStatus")) {
                var error = $root.gaia.SystemStatus.verify(message.systemStatus);
                if (error)
                    return "systemStatus." + error;
            }
            return null;
        };

        /**
         * Creates a Status message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof gaia.Status
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {gaia.Status} Status
         */
        Status.fromObject = function fromObject(object) {
            if (object instanceof $root.gaia.Status)
                return object;
            var message = new $root.gaia.Status();
            if (object.authenticationToken != null)
                message.authenticationToken = String(object.authenticationToken);
            if (object.localTimestamp != null)
                message.localTimestamp = String(object.localTimestamp);
            if (object.currentConfig != null) {
                if (typeof object.currentConfig !== "object")
                    throw TypeError(".gaia.Status.currentConfig: object expected");
                message.currentConfig = $root.gaia.Config.fromObject(object.currentConfig);
            }
            if (object.systemStatus != null) {
                if (typeof object.systemStatus !== "object")
                    throw TypeError(".gaia.Status.systemStatus: object expected");
                message.systemStatus = $root.gaia.SystemStatus.fromObject(object.systemStatus);
            }
            return message;
        };

        /**
         * Creates a plain object from a Status message. Also converts values to other types if specified.
         * @function toObject
         * @memberof gaia.Status
         * @static
         * @param {gaia.Status} message Status
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Status.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.authenticationToken = "";
                object.localTimestamp = "";
                object.currentConfig = null;
                object.systemStatus = null;
            }
            if (message.authenticationToken != null && message.hasOwnProperty("authenticationToken"))
                object.authenticationToken = message.authenticationToken;
            if (message.localTimestamp != null && message.hasOwnProperty("localTimestamp"))
                object.localTimestamp = message.localTimestamp;
            if (message.currentConfig != null && message.hasOwnProperty("currentConfig"))
                object.currentConfig = $root.gaia.Config.toObject(message.currentConfig, options);
            if (message.systemStatus != null && message.hasOwnProperty("systemStatus"))
                object.systemStatus = $root.gaia.SystemStatus.toObject(message.systemStatus, options);
            return object;
        };

        /**
         * Converts this Status to JSON.
         * @function toJSON
         * @memberof gaia.Status
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Status.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        return Status;
    })();

    return gaia;
})();

module.exports = $root;
