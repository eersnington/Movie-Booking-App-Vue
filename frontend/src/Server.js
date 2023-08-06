import axios from 'axios'

export default () => {
    return axios.create({
        baseURL: `http://localhost:5001/`,
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
    })
}