export default {
    getFilepath(filepath) {
        if (!filepath) {
            return "https://i.pinimg.com/originals/10/b2/f6/10b2f6d95195994fca386842dae53bb2.png"
        }
        return "http://localhost/" + filepath
    }
}