import axios from "axios";

export default new (class TodosService {
  async getTodos(listID) {
    const resp = axios.get(`${process.env.VUE_APP_SERVER}/lists/todos/${listID}`);
    return (await resp).data;
  }

  async createTodo(listID, description) {
    const resp = axios.put(`${process.env.VUE_APP_SERVER}/lists/todos/${listID}`, {
      description: description,
    });
    return (await resp).data;
  }

  async getTodo(listID, todoID) {
    const resp = axios.get(`${process.env.VUE_APP_SERVER}/lists/todos/${listID}/${todoID}`);
    return (await resp).data;
  }

  async deleteTodo(listID, todoID) {
    const resp = axios.delete(`${process.env.VUE_APP_SERVER}/lists/todos/${listID}/${todoID}`);
    return (await resp).data;
  }

  async patchTodo(listID, todoID, newDescription, newIsDone) {
    const resp = axios.patch(`${process.env.VUE_APP_SERVER}/lists/todos/${listID}/${todoID}`, {
      description: newDescription,
      is_done: newIsDone,
    });
    return (await resp).data;
  }
})();
