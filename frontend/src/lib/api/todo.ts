
import type { createListType, updateStatus } from "../types/todo";
import { axiosInstance } from "./axios";
//create list
export async function createList(data:createListType){
    const result = await axiosInstance.post('/todos',data)
    return result.data
}

//get lists
export async function getLists() {
  const result = await axiosInstance.get('/todos');
  return result.data;
}
//update status
export async function updateTodoStatus({ id, status }: updateStatus) {
  const result = await axiosInstance.patch(`/todo/${id}`, { status });
  return result.data;
}