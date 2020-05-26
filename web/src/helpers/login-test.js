import accessToken from "./access-token";
import axios from "axios";

export const loginTest = async () => {
    if (accessToken.getToken()) {
        try {
            const response = await axios.get('/api/check_authorization/');
            if (response.status >= 400) {
                throw new Error("Error")
            }
        } catch (e) {
            accessToken.removeToken();
        }
    }
};
