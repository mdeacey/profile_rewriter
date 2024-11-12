/**
 * Logger module to handle logging at various levels.
 * Logs messages to the server or console, detecting the original caller file.
 */

const LOGGING_ENDPOINT = '/log';

function getOriginalCallerFile() {
    const error = new Error();
    const stackLines = error.stack.split('\n');
    // Find the first stack line outside `logger.js`
    for (let i = 2; i < stackLines.length; i++) {
        const line = stackLines[i];
        if (!line.includes('logger.js')) { // Skip any calls from this file
            const matches = line.match(/at\s+(.*?):(\d+):(\d+)/); // Extract file path
            if (matches) {
                const filePath = matches[1];
                return filePath.substring(filePath.lastIndexOf('/') + 1); // Extract only the file name
            }
        }
    }
    return 'unknown';
}

function log(level, message) {
    const fileName = getOriginalCallerFile(); // Detect the original caller
    const formattedMessage = `${fileName} - ${message}`;
    const prefixedMessage = `JavaScript: ${formattedMessage}`;
    const payload = {
        level: level,
        message: formattedMessage,
        fileName: fileName,
    };

    // Output to the console in the desired format
    console.log(`app-1  | ${level.toUpperCase()} - ${formattedMessage}`);

    // Send log to server
    fetch(LOGGING_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
        .then((response) => {
            if (!response.ok) {
                console.error(
                    `Failed to send ${level} log to server: ${response.statusText}`
                );
            } else {
                console.info(`Log (${level}) sent to server successfully.`);
            }
        })
        .catch((error) => {
            console.error(`Error sending ${level} log to server:`, error);
        });
}

// Helper functions for different levels of logging
log.debug = (message) => log('debug', message);
log.info = (message) => log('info', message);
log.warn = (message) => log('warn', message);
log.error = (message) => log('error', message);
log.critical = (message) => log('critical', message);