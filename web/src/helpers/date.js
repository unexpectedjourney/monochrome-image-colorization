export default {
    getDate(date) {
        if (date) {
            return date.split("T")[0];
        }
        return new Date().toISOString().split("T")[0];
    }
}