import accessToken from "./access-token";
import axios from "axios";

export const loginTest = async () => {
    if (accessToken.getToken()) {
        try {
            const response = await axios.get('/user/');
            console.log('user response', response);
        } catch (e) {
            if (e.response.status === 401) {
                // accessToken.removeToken();
            }
        }
    }
};
