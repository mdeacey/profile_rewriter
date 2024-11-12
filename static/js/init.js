// Initialize all managers on page load
window.addEventListener('DOMContentLoaded', () => {
    TextareaManager.init();
    ButtonManager.init();
    LoadingManager.init();
    FormNavigationManager.init();
    FormManager.init();
    log.debug('All managers initialized.');
});
