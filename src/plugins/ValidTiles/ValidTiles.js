/* globals define */
/* eslint-env node */

/**
 * Generated by PluginGenerator 2.20.5 from webgme on Thu Dec 07 2023 02:16:19 GMT-0600 (Central Standard Time).
 * A plugin that inherits from the PluginBase. To see source code documentation about available
 * properties and methods visit %host%/docs/source/PluginBase.html.
 */

define([
    'q',
    'plugin/PluginConfig',
    'text!./metadata.json',
    'plugin/PluginBase',
    'module'
], function (
    Q,
    PluginConfig,
    pluginMetadata,
    PluginBase,
    module) {
    'use strict';

    pluginMetadata = JSON.parse(pluginMetadata);
    const path = require('path');
    // Modify these as needed..
    const START_PORT = 5555;
    const COMMAND = 'python';
    const SCRIPT_FILE = path.join(path.dirname(module.uri), 'run_plugin.py');

    /**
     * Initializes a new instance of PythonBindings.
     * @class
     * @augments {PluginBase}
     * @classdesc This class represents the plugin PythonBindings.
     * @constructor
     */
    function ValidTiles() {
        // Call base class' constructor.
        PluginBase.call(this);
        this.pluginMetadata = pluginMetadata;
    }

    /**
     * Metadata associated with the plugin. Contains id, name, version, description, icon, configStructue etc.
     * This is also available at the instance at this.pluginMetadata.
     * @type {object}
     */
    ValidTiles.metadata = pluginMetadata;

    // Prototypical inheritance from PluginBase.
    ValidTiles.prototype = Object.create(PluginBase.prototype);
    ValidTiles.prototype.constructor = ValidTiles;

    /**
     * Main function for the plugin to execute. This will perform the execution.
     * Notes:
     * - Always log with the provided logger.[error,warning,info,debug].
     * - Do NOT put any user interaction logic UI, etc. inside this method.
     * - callback always has to be called even if error happened.
     *
     * @param {function(null|Error|string, plugin.PluginResult)} callback - the result callback
     */
    ValidTiles.prototype.main = function (callback) {
        const CoreZMQ = require('webgme-bindings').CoreZMQ;
        const cp = require('child_process');
        const logger = this.logger;

        // due to the limited options on the script return values, we need this hack
        this.result.setSuccess(null);

        const callScript = (program, scriptPath, port) => {
            let deferred = Q.defer(),
                options = {},
                args = [
                    scriptPath,
                    port,
                    `"${this.commitHash}"`,
                    `"${this.branchName}"`,
                    `"${this.core.getPath(this.activeNode)}"`,
                    `"${this.activeSelection.map(node => this.core.getPath(node)).join(',')}"`,
                    `"${this.namespace}"`,
                ];

            const childProc = cp.spawn(program, args, options);

            childProc.stdout.on('data', data => {
                logger.info(data.toString());
                // logger.debug(data.toString());
            });

            childProc.stderr.on('data', data => {
                logger.error(data.toString());
            });

            childProc.on('close', (code) => {
                if (code > 0) {
                    // This means an execution error or crash, so we are failing the plugin
                    deferred.reject(new Error(`${program} ${args.join(' ')} exited with code ${code}.`));
                    this.result.setSuccess(false);
                } else {
                    if(this.result.getSuccess() === null) {
                        // The result have not been set inside the python, but it suceeded, so we go with the true value
                        this.result.setSuccess(true);
                    }
                    deferred.resolve();
                }
            });

            childProc.on('error', (err) => {
                // This is a hard execution error, like the child process cannot be instantiated...
                logger.error(err);
                this.result.setSuccess(false);
                deferred.reject(err);
            });

            return deferred.promise;
        };

        const corezmq = new CoreZMQ(this.project, this.core, this.logger, {port: START_PORT, plugin: this});
        corezmq.startServer()
            .then((port) => {
                logger.info(`zmq-server listening at port ${port}`);
                return callScript(COMMAND, SCRIPT_FILE, port);
            })
            .then(() => {
                return corezmq.stopServer();
            })
            .then(() => {
                callback(null, this.result);
            })
            .catch((err) => {
                this.logger.error(err.stack);
                corezmq.stopServer()
                    .finally(() => {
                        // Result success is false at invocation.
                        callback(err, this.result);
                    });
            });
    };

    return ValidTiles;
});
