export default {
    setToken(token) {
        window.localStorage.setItem('access_token', token);
    },
    getToken() {
        return window.localStorage.getItem('access_token');
    },
    removeToken() {
        window.localStorage.removeItem('access_token');
    },
};
