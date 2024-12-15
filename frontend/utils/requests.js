import axios from "axios";

const githubAPI = axios.create({
  baseURL: "https://api.github.com",
  headers: {
    "Content-Type": "application/json",
  },
});

const getRepos = async (username) => {
  const response = await githubAPI.get(`/users/${username}/repos`);
  return response.data;
};

const userInfo = async (username) => {
  const response = await githubAPI.get(`/users/${username}`);
  return response.data;
};

const userExists = async (username) => {
  const response = await githubAPI.get(`/users/${username}`);
  return response.status;
};

export { getRepos, userInfo, userExists };
