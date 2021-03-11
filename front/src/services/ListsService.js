import axios from "axios";
import { server } from "@/services/config";

export default new (class ListsService {
  async getLists() {
    const resp = axios.get(`${server}/lists`);
    return (await resp).data;
  }

  async createList(listTitle) {
    const resp = axios.put(
      `${server}/lists`,
      { title: listTitle },
      { headers: { "Content-Type": "application/json" } }
    );
    return (await resp).data;
  }

  async getList(listID) {
    const resp = axios.get(`${server}/lists/${listID}`);
    return (await resp).data;
  }

  async patchList(listID, newTitle) {
    const resp = axios.patch(
      `${server}/lists/${listID}`,
      { title: newTitle },
      { headers: { "Content-Type": "application/json" } }
    );
    return (await resp).data;
  }

  async deleteList(listID) {
    const resp = axios.delete(`${server}/lists/${listID}`);
    return (await resp).data;
  }
})();
