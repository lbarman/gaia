import * as $protobuf from "protobufjs";
/** Namespace gaia. */
export namespace gaia {

    /** Properties of a Config. */
    interface IConfig {

        /** Config feedingModuleActivated */
        feedingModuleActivated?: (boolean|null);

        /** Config wateringModuleActivated */
        wateringModuleActivated?: (boolean|null);

        /** Config feedingModuleCronstring */
        feedingModuleCronstring?: (string|null);

        /** Config wateringModuleCronstring */
        wateringModuleCronstring?: (string|null);

        /** Config wateringPump_1Duration */
        wateringPump_1Duration?: (number|null);

        /** Config wateringPump_2Duration */
        wateringPump_2Duration?: (number|null);

        /** Config wateringPump_3Duration */
        wateringPump_3Duration?: (number|null);

        /** Config wateringPump_4Duration */
        wateringPump_4Duration?: (number|null);
    }

    /** Represents a Config. */
    class Config implements IConfig {

        /**
         * Constructs a new Config.
         * @param [properties] Properties to set
         */
        constructor(properties?: gaia.IConfig);

        /** Config feedingModuleActivated. */
        public feedingModuleActivated: boolean;

        /** Config wateringModuleActivated. */
        public wateringModuleActivated: boolean;

        /** Config feedingModuleCronstring. */
        public feedingModuleCronstring: string;

        /** Config wateringModuleCronstring. */
        public wateringModuleCronstring: string;

        /** Config wateringPump_1Duration. */
        public wateringPump_1Duration: number;

        /** Config wateringPump_2Duration. */
        public wateringPump_2Duration: number;

        /** Config wateringPump_3Duration. */
        public wateringPump_3Duration: number;

        /** Config wateringPump_4Duration. */
        public wateringPump_4Duration: number;

        /**
         * Creates a new Config instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Config instance
         */
        public static create(properties?: gaia.IConfig): gaia.Config;

        /**
         * Encodes the specified Config message. Does not implicitly {@link gaia.Config.verify|verify} messages.
         * @param message Config message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: gaia.IConfig, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Config message, length delimited. Does not implicitly {@link gaia.Config.verify|verify} messages.
         * @param message Config message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: gaia.IConfig, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Config message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Config
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): gaia.Config;

        /**
         * Decodes a Config message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Config
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): gaia.Config;

        /**
         * Verifies a Config message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Config message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Config
         */
        public static fromObject(object: { [k: string]: any }): gaia.Config;

        /**
         * Creates a plain object from a Config message. Also converts values to other types if specified.
         * @param message Config
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: gaia.Config, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Config to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };
    }

    /** Properties of a SystemStatus. */
    interface ISystemStatus {

        /** SystemStatus uptime */
        uptime?: (string|null);

        /** SystemStatus memory */
        memory?: (string|null);

        /** SystemStatus diskUsage */
        diskUsage?: (string|null);

        /** SystemStatus processes */
        processes?: (string|null);
    }

    /** Represents a SystemStatus. */
    class SystemStatus implements ISystemStatus {

        /**
         * Constructs a new SystemStatus.
         * @param [properties] Properties to set
         */
        constructor(properties?: gaia.ISystemStatus);

        /** SystemStatus uptime. */
        public uptime: string;

        /** SystemStatus memory. */
        public memory: string;

        /** SystemStatus diskUsage. */
        public diskUsage: string;

        /** SystemStatus processes. */
        public processes: string;

        /**
         * Creates a new SystemStatus instance using the specified properties.
         * @param [properties] Properties to set
         * @returns SystemStatus instance
         */
        public static create(properties?: gaia.ISystemStatus): gaia.SystemStatus;

        /**
         * Encodes the specified SystemStatus message. Does not implicitly {@link gaia.SystemStatus.verify|verify} messages.
         * @param message SystemStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: gaia.ISystemStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified SystemStatus message, length delimited. Does not implicitly {@link gaia.SystemStatus.verify|verify} messages.
         * @param message SystemStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: gaia.ISystemStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a SystemStatus message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns SystemStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): gaia.SystemStatus;

        /**
         * Decodes a SystemStatus message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns SystemStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): gaia.SystemStatus;

        /**
         * Verifies a SystemStatus message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a SystemStatus message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns SystemStatus
         */
        public static fromObject(object: { [k: string]: any }): gaia.SystemStatus;

        /**
         * Creates a plain object from a SystemStatus message. Also converts values to other types if specified.
         * @param message SystemStatus
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: gaia.SystemStatus, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this SystemStatus to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };
    }

    /** Properties of a Status. */
    interface IStatus {

        /** Status authenticationToken */
        authenticationToken?: (string|null);

        /** Status localTimestamp */
        localTimestamp?: (string|null);

        /** Status currentConfig */
        currentConfig?: (gaia.IConfig|null);

        /** Status systemStatus */
        systemStatus?: (gaia.ISystemStatus|null);
    }

    /** Represents a Status. */
    class Status implements IStatus {

        /**
         * Constructs a new Status.
         * @param [properties] Properties to set
         */
        constructor(properties?: gaia.IStatus);

        /** Status authenticationToken. */
        public authenticationToken: string;

        /** Status localTimestamp. */
        public localTimestamp: string;

        /** Status currentConfig. */
        public currentConfig?: (gaia.IConfig|null);

        /** Status systemStatus. */
        public systemStatus?: (gaia.ISystemStatus|null);

        /**
         * Creates a new Status instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Status instance
         */
        public static create(properties?: gaia.IStatus): gaia.Status;

        /**
         * Encodes the specified Status message. Does not implicitly {@link gaia.Status.verify|verify} messages.
         * @param message Status message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: gaia.IStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Status message, length delimited. Does not implicitly {@link gaia.Status.verify|verify} messages.
         * @param message Status message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: gaia.IStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Status message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): gaia.Status;

        /**
         * Decodes a Status message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): gaia.Status;

        /**
         * Verifies a Status message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Status message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Status
         */
        public static fromObject(object: { [k: string]: any }): gaia.Status;

        /**
         * Creates a plain object from a Status message. Also converts values to other types if specified.
         * @param message Status
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: gaia.Status, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Status to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };
    }
}
