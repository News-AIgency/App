import axios from "axios";

export default() => {
  return axios.create({
    baseURL: "https://147.175.151.160/api/"
  });
};
