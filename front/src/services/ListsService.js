import axios from "axios";

export default new (class ListsService {
  async getLists() {
    const resp = axios.get(`${process.env.VUE_APP_SERVER}/lists`);
    return (await resp).data;
  }

  async createList(listTitle) {
    const resp = axios.put(`${process.env.VUE_APP_SERVER}/lists`, { title: listTitle });
    return (await resp).data;
  }

  async getList(listID) {
    const resp = axios.get(`${process.env.VUE_APP_SERVER}/lists/${listID}`);
    return (await resp).data;
  }

  async deleteList(listID) {
    const resp = axios.delete(`${process.env.VUE_APP_SERVER}/lists/${listID}`);
    return (await resp).data;
  }

  async patchList(listID, newTitle) {
    const resp = axios.patch(`${process.env.VUE_APP_SERVER}/lists/${listID}`, { title: newTitle });
    return (await resp).data;
  }
})();
