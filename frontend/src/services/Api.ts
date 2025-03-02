import axios from "axios";

export default() => {
  return axios.create({
    baseURL: "https://team04-24.studenti.fiit.stuba.sk/api/"
  });
};
