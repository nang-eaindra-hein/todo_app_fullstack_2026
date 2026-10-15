
import type { createListType, TodosResponse, TodoStatus, updateStatusType } from "../types/todo";
import { axiosInstance } from "./axios";


//create list
export async function createList(data:createListType){
    const result = await axiosInstance.post('/todo',data)
    return result.data
}

//get lists
export async function getLists(status?: TodoStatus): Promise<TodosResponse> {
	const result = await axiosInstance.get('/todos', {
		params: status ? { status } : {}
	});
	return result.data;
}

//update status
export async function updateTodoStatus({ id, status }: updateStatusType) {
  const result = await axiosInstance.patch(`/update_status/${id}`, { status });
  return result.data;
}
//update data in a list
export async function updateList({ id, title, description, status }: {
  id: number; title: string; description: string; status: string;
}) {
  const result = await axiosInstance.put(`/todos/${id}`, { title, description, status });
  return result.data;
}

//delete id
export async function deleteList({id}:{id:number}) {
  const result = await axiosInstance.delete(`/delete_todo/${id}`);
  return result.data;
}

//delete all
export async function deleteLists() {
  const result = await axiosInstance.delete('/delete_todos');
  return result.data;
}