import axios from "axios";

export default() => {
  return axios.create({
    baseURL: "http://team04-24.studenti.fiit.stuba.sk/api/"
  });
};
