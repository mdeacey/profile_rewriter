/**
 * Parent Manager: ButtonManager
 * Handles button-related behaviors, including simulating button presses.
 */
const ButtonManager = {
    init() {
        log.debug('ButtonManager: Initializing button listeners.');
        document.querySelectorAll('button').forEach((button) => {
            button.addEventListener('click', () => {
                this.simulateButtonPress(button);
            });
            log.debug('ButtonManager: Added click listener to button.');
        });
    },

    simulateButtonPress(button) {
        try {
            log.debug('ButtonManager: Simulating button press.');
            button.style.transform = 'scale(0.98)'; // Button press effect
            setTimeout(() => {
                button.style.transform = ''; // Reset the button scaling
                log.debug('ButtonManager: Button press simulation completed.');
            }, 100);
        } catch (err) {
            log.error(`ButtonManager: An error occurred during button simulation - ${err.message}`);
        }
    }
};