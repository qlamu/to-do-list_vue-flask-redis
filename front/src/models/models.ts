export interface Login {
  jwt: string
}

export interface Todo {
  todo_id: number | string,
  description: string,
  is_done: number | string
}