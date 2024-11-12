/**
Parent Manager: LoadingManager
Handles loading message and elapsed time display.
*/

const LoadingManager = {
    timers: [],
    elapsedInterval: null,
    startTime: null,
    totalSteps: 0,
    steps: [],
    barWidth: 20,
    currentMessage: '',
    currentProgressBar: '',
    initialized: false,
    activeStep: 0,
    loading: false,
    abortController: null,

    init() {
        if (this.initialized) {
            log.warn('LoadingManager: Already initialized.');
            return;
        }
        this.bindFormSubmit();
        this.initialized = true;
        log.debug('LoadingManager: Initialized.');
    },

    reset() {
        log.debug('LoadingManager: Resetting state.');
        if (this.abortController) {
            this.abortController.abort();
            log.debug('LoadingManager: Aborted previous operations.');
        }
        this.clearAllTimers();
        this.startTime = null;
        this.totalSteps = 0;
        this.steps = [];
        this.currentMessage = '';
        this.currentProgressBar = '';
        this.activeStep = 0;
        this.loading = false;
        this.abortController = null;

        const loadingProgressElement = document.getElementById('loadingProgressMessage');
        const loadingMessageElement = document.getElementById('loadingMessage');
        if (loadingProgressElement) {
            loadingProgressElement.innerText = '';
            log.debug('Loading progress element cleared.');
        }
        if (loadingMessageElement) {
            loadingMessageElement.style.display = 'none';
            log.debug('Loading message element hidden.');
        }
        log.debug('LoadingManager: All states reset.');
    },

    initialize(numOutputs = 1) {
        this.reset();
        this.startTime = Date.now();
        this.currentMessage = '';
        this.currentProgressBar = '';
        this.activeStep = 0;
        this.loading = true;
        numOutputs = Math.max(1, parseInt(numOutputs, 10) || 1);

        log.debug(`LoadingManager: Initializing loader for ${numOutputs} output(s).`);

        const initialSteps = [
            ['Extracting parameters...', this.getRandomInRange(100, 250)],
            ['Constructing prompt...', this.getRandomInRange(100, 250)],
            ['Making API request...', this.getRandomInRange(2000, 2500)],
        ];

        const outputSteps = Array.from({ length: numOutputs }, (_, i) => [
            [`Post-processing output ${i + 1}...`, this.getRandomInRange(250, 500)],
            [`Validating output ${i + 1}...`, this.getRandomInRange(250, 500)],
        ]).flat();

        const closingSteps = [
            ['Final validation...', this.getRandomInRange(100, 250)],
            ['Calculating token usage and cost...', this.getRandomInRange(100, 250)],
            ['Finalizing...', Infinity],
        ];

        this.steps = [...initialSteps, ...outputSteps, ...closingSteps];
        this.totalSteps = this.steps.length;

        log.debug(`LoadingManager: Steps initialized (${this.totalSteps} total steps).`);
    },

    async showLoading(numOutputs = 1, submitForm) {
        if (this.loading) {
            log.warn('LoadingManager: Restarting loading process...');
            this.reset();
        }

        log.debug('LoadingManager: Starting new loading process...');
        this.initialize(numOutputs);

        const loadingMessageElement = document.getElementById('loadingMessage');
        const loadingProgressElement = document.getElementById('loadingProgressMessage');
        if (loadingMessageElement) {
            loadingMessageElement.style.display = 'block';
            log.debug('Loading message element shown.');
        }
        if (loadingProgressElement) {
            loadingProgressElement.innerText = '';
        }

        this.startElapsedTimeUpdater();

        try {
            this.abortController = new AbortController();
            await this.runStepsSequentially(this.abortController.signal);

            this.displayFinalizingState();
            submitForm();
        } catch (error) {
            if (error.name === 'AbortError') {
                log.debug('LoadingManager: Loading process aborted.');
            } else {
                log.error(`LoadingManager: Error encountered during steps: ${error}`);
            }
        } finally {
            this.loading = false;
        }
    },

    async runStepsSequentially(signal) {
        for (this.activeStep = 1; this.activeStep <= this.totalSteps; this.activeStep++) {
            if (signal.aborted) throw new Error('AbortError');

            const [message, duration] = this.steps[this.activeStep - 1];
            this.currentMessage = `${message} [${this.activeStep}/${this.totalSteps}]`;
            this.updateStep(this.activeStep);
            log.debug(`Processing step ${this.activeStep}/${this.totalSteps}: "${message}" | Expected Duration: ${duration} ms`);
            
            if (duration !== Infinity) {
                await this.delay(duration, signal);
            } else {
                break;
            }
            log.debug(`Step ${this.activeStep}/${this.totalSteps} completed after ${duration} ms.`);
        }
    },

    displayFinalizingState() {
        log.debug('LoadingManager: Displaying "Finalizing..." state indefinitely.');
        const loadingProgressElement = document.getElementById('loadingProgressMessage');
        if (loadingProgressElement) {
            const elapsedTime = ((Date.now() - this.startTime) / 1000).toFixed(1);
            const elapsedMessage = `Loading [${elapsedTime}s]...`;
            const finalMessage = `Finalizing... [${this.totalSteps}/${this.totalSteps}]`;
            const combinedDisplay = `${elapsedMessage}\n${finalMessage}\n${this.buildProgressBar(100)}`;
            loadingProgressElement.innerText = combinedDisplay;
        }
    },

    updateStep(stepNumber) {
        if (stepNumber > this.totalSteps) {
            log.error(`Step out of bounds: ${stepNumber} exceeds total step count of ${this.totalSteps}. Aborting.`);
            return;
        }

        const percentageComplete = (stepNumber / this.totalSteps) * 100;
        this.currentProgressBar = this.buildProgressBar(percentageComplete);
        log.debug(`LoadingManager: Updated step ${stepNumber}/${this.totalSteps} - Message: "${this.currentMessage}"`);

        const loadingProgressElement = document.getElementById('loadingProgressMessage');
        if (loadingProgressElement) {
            const elapsedTime = ((Date.now() - this.startTime) / 1000).toFixed(1);
            const elapsedMessage = `Loading [${elapsedTime}s]...`;
            const combinedDisplay = `${elapsedMessage}\n${this.currentMessage}\n${this.currentProgressBar}`;
            loadingProgressElement.innerText = combinedDisplay;
        }
    },

    buildProgressBar(percentageComplete) {
        const completedChars = Math.floor((percentageComplete / 100) * this.barWidth);
        const remainingChars = this.barWidth - completedChars;
        const percentageDisplay = `${percentageComplete.toFixed(0)}%`;
        return `[${'#'.repeat(completedChars)}${'-'.repeat(remainingChars)}] ${percentageDisplay}`;
    },

    startElapsedTimeUpdater() {
        this.clearAllTimers();

        this.elapsedInterval = setInterval(() => {
            const elapsedTime = ((Date.now() - this.startTime) / 1000).toFixed(1);
            const elapsedMessage = `Loading [${elapsedTime}s]...`;

            const loadingProgressElement = document.getElementById('loadingProgressMessage');
            if (loadingProgressElement) {
                loadingProgressElement.innerText = `${elapsedMessage}\n${this.currentMessage}\n${this.currentProgressBar}`;
                log.debug(`UI updated with elapsed time: ${elapsedTime}s`);
            }
        }, 100);
    },

    clearAllTimers() {
        if (this.elapsedInterval) {
            clearInterval(this.elapsedInterval);
            this.elapsedInterval = null;
            log.debug('Elapsed time updater cleared.');
        }
        this.timers.forEach(clearTimeout);
        this.timers = [];
        log.debug('All timers cleared.');
    },

    delay(ms, signal) {
        return new Promise((resolve, reject) => {
            if (signal.aborted) return reject(new Error('AbortError'));
            const timer = setTimeout(() => {
                if (signal.aborted) return reject(new Error('AbortError'));
                resolve();
            }, ms);
            this.timers.push(timer);
        });
    },

    getRandomInRange(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    bindFormSubmit() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', event => {
                event.preventDefault();
                const submitForm = () => form.submit();
                const numOutputsInput = document.getElementById('num_outputs');
                const numOutputs = Math.max(1, parseInt(numOutputsInput?.value, 10) || 1);

                log.debug(`LoadingManager: Form submitted with ${numOutputs} output(s).`);
                this.showLoading(numOutputs, submitForm);
            });
            log.debug('LoadingManager: Form submit event listener attached.');
        } else {
            log.error('LoadingManager: Form element not found.');
        }
    },
};