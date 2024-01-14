// services/FoodService.ts
import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8080",
    withCredentials: true,
})

const getFoodItems = async () => {
    try {
        return axiosInstance.get("/getrecipes").then(resp => {
            console.log(resp);
            return resp
        })
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

export default getFoodItems;
