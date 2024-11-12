/**
 * Parent Manager: FormManager
 * Manages form fields, cookies, and URL parameters.
 */
const FormManager = {
    fields: ['responder_name', 'dialect', 'formality', 'tone', 'creativity', 'channel', 'greetings', 'sentence_limit', 'num_outputs', 'uniqueness_attempts'],

    init() {
        log.debug('FormManager: Initializing form behaviors.');
        this.addInputListeners();
    },

    addInputListeners() {
        this.fields.forEach((fieldId) => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', () => {
                    const value = this.getFieldValue(fieldId);
                    this.setCookie(fieldId, value);
                    this.updateURLParams();
                });
            }
        });
        this.addUniquenessAttemptsListener();
    },

    addUniquenessAttemptsListener() {
        const inputTextarea = document.getElementById('inputTextarea');
        const attemptsInput = document.getElementById('uniqueness_attempts');
        inputTextarea.addEventListener('input', () => {
            this.updateUniquenessAttempts(inputTextarea.value.length);
        });
        this.updateUniquenessAttempts(inputTextarea.value.length);
    },

    updateUniquenessAttempts(textLength) {
        const attemptsInput = document.getElementById('uniqueness_attempts');
        let attempts = 5;
        attempts = Math.max(1, 5 - Math.floor(textLength / 75));
        attemptsInput.value = attempts;
        log.debug(`FormManager: Uniqueness attempts automatically set to ${attempts} based on input length.`);
    },

    getFieldValue(fieldId) {
        log.debug(`FormManager: Retrieving value for "${fieldId}".`);
        const field = document.getElementById(fieldId);
        return field ? field.value.toLowerCase() : '';
    },

    setCookie(name, value) {
        log.debug(`FormManager: Setting cookie "${name}" to "${value}".`);
        document.cookie = `${name}=${value}; path=/; SameSite=Lax;`;
    },
    
    updateURLParams() {
        log.debug('FormManager: Updating URL parameters.');
        const params = new URLSearchParams(window.location.search);
        this.fields.forEach((fieldId) => {
            const value = this.getFieldValue(fieldId);
            if (value) {
                params.set(fieldId, value);
            }
        });
        window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
    }
};